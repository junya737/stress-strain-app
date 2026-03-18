"""解析サービス.

解析フローの調停を行う。router ↔ analysis の仲介に徹する。
"""

import uuid
from dataclasses import dataclass, field

import numpy as np

from app.analysis.converter import engineering_to_true
from app.analysis.fracture import detect_fracture
from app.analysis.toughness import calculate_toughness
from app.analysis.uts import calculate_uts
from app.analysis.yield_strength import calculate_yield_strength
from app.analysis.youngs_modulus import calculate_youngs_modulus
from app.core.errors import AnalysisWarning
from app.domain.mechanical_props import MechanicalProperties
from app.domain.specimen import SpecimenData
from app.io.csv_parser import extract_arrays
from app.schemas.analysis import (
    AnalysisRequest,
    AnalysisResponse,
    AnnotationPoint,
    CalculationContextResponse,
    CurveDataResponse,
    MechanicalPropertiesResponse,
    RecalculateRequest,
    WarningResponse,
)
from app.services.dataset_service import get_dataframe
from app.utils.unit_converter import (
    convert_strain_to_dimensionless,
    convert_stress_to_mpa,
)


@dataclass
class AnalysisRecord:
    """解析記録.

    再計算時に元データを保持するための構造体。

    Attributes:
        specimen: 試験片データ
        request: 解析リクエスト
        response: 解析レスポンス
    """

    specimen: SpecimenData
    request: AnalysisRequest
    response: AnalysisResponse


@dataclass
class AnalysisStore:
    """解析結果のインメモリ保管庫."""

    records: dict[str, AnalysisRecord] = field(default_factory=dict)


_store = AnalysisStore()


def get_analysis_store() -> AnalysisStore:
    """解析ストアを取得する."""
    return _store


def run_analysis(request: AnalysisRequest) -> AnalysisResponse:
    """解析を実行する.

    Args:
        request: 解析リクエスト

    Returns:
        AnalysisResponse
    """
    mapping = request.column_mapping
    df = get_dataframe(request.dataset_id)

    # 配列抽出
    strain_raw, stress_raw = extract_arrays(
        df=df,
        strain_col=mapping.strain_column,
        stress_col=mapping.stress_column,
        load_col=mapping.load_column,
        displacement_col=mapping.displacement_column,
        cross_section_area=mapping.cross_section_area,
        gauge_length=mapping.gauge_length,
    )

    # 単位変換
    strain = convert_strain_to_dimensionless(strain_raw, mapping.strain_unit)
    stress = convert_stress_to_mpa(stress_raw, mapping.stress_unit)

    # トリミング
    if request.trim_range is not None:
        trim_mask = (
            (strain >= request.trim_range[0])
            & (strain <= request.trim_range[1])
        )
        strain = strain[trim_mask]
        stress = stress[trim_mask]

    # 試験片データ
    specimen = SpecimenData(
        name=request.specimen_name,
        strain=strain,
        stress=stress,
        raw_strain=strain_raw,
        raw_stress=stress_raw,
    )

    # 解析実行
    props, all_warnings = _compute_properties(
        strain=strain,
        stress=stress,
        strain_range=request.youngs_modulus_strain_range,
        yield_offset=request.yield_offset,
    )

    # 変換履歴
    conversions: list[str] = []
    if mapping.strain_unit.value != "dimensionless":
        conversions.append(
            f"strain: {mapping.strain_unit.value} -> dimensionless"
        )
    if mapping.stress_unit.value != "MPa":
        conversions.append(
            f"stress: {mapping.stress_unit.value} -> MPa"
        )
    if mapping.load_column and mapping.cross_section_area:
        conversions.append("load -> stress (load / cross_section_area)")
    if mapping.displacement_column and mapping.gauge_length:
        conversions.append(
            "displacement -> strain (displacement / gauge_length)"
        )

    # レスポンス構築
    analysis_id = str(uuid.uuid4())

    # 注釈点
    annotation_points: list[AnnotationPoint] = [
        AnnotationPoint(
            label="UTS",
            strain=props.uts.strain_at_uts,
            stress=props.uts.value_mpa,
        ),
        AnnotationPoint(
            label="Fracture",
            strain=props.fracture.strain,
            stress=props.fracture.stress_mpa,
        ),
    ]
    if props.yield_strength.value_mpa is not None:
        annotation_points.append(
            AnnotationPoint(
                label="0.2% Yield",
                strain=float(
                    props.yield_strength.value_mpa / props.youngs_modulus.slope_mpa
                    + props.yield_strength.offset_used
                ),
                stress=props.yield_strength.value_mpa,
            )
        )

    # 回帰直線データ
    ym = props.youngs_modulus
    reg_strain_start = ym.fit_range[0]
    reg_strain_end = ym.fit_range[1]
    regression_line = {
        "strain": [reg_strain_start, reg_strain_end],
        "stress": [
            ym.slope_mpa * reg_strain_start + ym.intercept_mpa,
            ym.slope_mpa * reg_strain_end + ym.intercept_mpa,
        ],
    }

    # オフセット直線データ
    offset = request.yield_offset
    offset_strain_start = offset
    offset_strain_end = float(strain[props.uts.index]) if len(strain) > 0 else 0.01
    offset_line = {
        "strain": [offset_strain_start, offset_strain_end],
        "stress": [
            ym.slope_mpa * (offset_strain_start - offset) + ym.intercept_mpa,
            ym.slope_mpa * (offset_strain_end - offset) + ym.intercept_mpa,
        ],
    }

    response = AnalysisResponse(
        analysis_id=analysis_id,
        specimen_name=request.specimen_name,
        results=MechanicalPropertiesResponse(
            youngs_modulus_gpa=props.youngs_modulus.value_gpa,
            yield_strength_02_mpa=props.yield_strength.value_mpa,
            ultimate_tensile_strength_mpa=props.uts.value_mpa,
            uniform_elongation_percent=props.uts.strain_at_uts * 100.0,
            fracture_strain_percent=props.fracture.strain * 100.0,
            toughness_mj_m3=props.toughness_mj_m3,
        ),
        calculation_context=CalculationContextResponse(
            youngs_modulus_fit_range=props.youngs_modulus.fit_range,
            youngs_modulus_r_squared=props.youngs_modulus.r_squared,
            youngs_modulus_data_points=props.youngs_modulus.data_points,
            youngs_modulus_method=props.youngs_modulus.method,
            yield_offset_used=request.yield_offset,
            yield_intersection_found=props.yield_strength.intersection_found,
            trim_range_applied=request.trim_range,
            input_units={
                "strain": mapping.strain_unit.value,
                "stress": mapping.stress_unit.value,
            },
            conversion_applied=conversions,
        ),
        curve_data=CurveDataResponse(
            strain=strain.tolist(),
            stress=stress.tolist(),
            curve_type="engineering",
            regression_line=regression_line,
            offset_line=offset_line,
            annotation_points=annotation_points,
        ),
        warnings=[
            WarningResponse(
                metric=w.metric,
                message=w.message,
                severity=w.severity,
            )
            for w in all_warnings
        ],
    )

    # 保存
    _store.records[analysis_id] = AnalysisRecord(
        specimen=specimen,
        request=request,
        response=response,
    )

    return response


def recalculate_analysis(
    analysis_id: str,
    request: RecalculateRequest,
) -> AnalysisResponse:
    """解析を再計算する.

    Args:
        analysis_id: 既存の解析ID
        request: 再計算リクエスト

    Returns:
        更新されたAnalysisResponse
    """
    assert analysis_id in _store.records, (
        f"Analysis '{analysis_id}' not found"
    )
    record = _store.records[analysis_id]

    # 元のリクエストを更新
    updated_request = AnalysisRequest(
        dataset_id=record.request.dataset_id,
        specimen_name=record.request.specimen_name,
        column_mapping=record.request.column_mapping,
        youngs_modulus_strain_range=request.youngs_modulus_strain_range,
        yield_offset=request.yield_offset,
        trim_range=request.trim_range,
    )

    return run_analysis(updated_request)


def get_analysis(analysis_id: str) -> AnalysisResponse:
    """解析結果を取得する.

    Args:
        analysis_id: 解析ID

    Returns:
        AnalysisResponse
    """
    assert analysis_id in _store.records, (
        f"Analysis '{analysis_id}' not found"
    )
    return _store.records[analysis_id].response


def _compute_properties(
    strain: np.ndarray,
    stress: np.ndarray,
    strain_range: tuple[float, float] | None,
    yield_offset: float,
) -> tuple[MechanicalProperties, list[AnalysisWarning]]:
    """全機械的特性を算出する."""
    all_warnings: list[AnalysisWarning] = []

    # ヤング率
    ym_result, ym_warnings = calculate_youngs_modulus(
        strain, stress, strain_range
    )
    all_warnings.extend(ym_warnings)

    # 0.2%耐力
    ys_result, ys_warnings = calculate_yield_strength(
        strain, stress,
        youngs_modulus_mpa=ym_result.slope_mpa,
        intercept_mpa=ym_result.intercept_mpa,
        offset=yield_offset,
    )
    all_warnings.extend(ys_warnings)

    # UTS
    uts_result = calculate_uts(strain, stress)

    # 破断点
    fracture_result = detect_fracture(strain, stress, uts_result.index)

    # 靱性
    toughness = calculate_toughness(strain, stress, fracture_result.index)

    props = MechanicalProperties(
        youngs_modulus=ym_result,
        yield_strength=ys_result,
        uts=uts_result,
        fracture=fracture_result,
        toughness_mj_m3=toughness,
        warnings=all_warnings,
    )

    return props, all_warnings
