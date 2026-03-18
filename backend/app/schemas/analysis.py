"""解析関連のPydanticスキーマ（API境界）."""

from pydantic import BaseModel

from app.schemas.dataset import ColumnMapping


class AnalysisRequest(BaseModel):
    """解析リクエスト.

    Attributes:
        dataset_id: データセットID
        specimen_name: 試験片名
        column_mapping: 列マッピング
        youngs_modulus_strain_range: ヤング率算出のひずみ範囲（手動指定時）
        yield_offset: 耐力のオフセット値（デフォルト0.2%）
        trim_range: データトリミング範囲
    """

    dataset_id: str
    specimen_name: str
    column_mapping: ColumnMapping
    youngs_modulus_strain_range: tuple[float, float] | None = None
    yield_offset: float = 0.002
    trim_range: tuple[float, float] | None = None


class MechanicalPropertiesResponse(BaseModel):
    """機械的特性レスポンス."""

    youngs_modulus_gpa: float
    yield_strength_02_mpa: float | None
    ultimate_tensile_strength_mpa: float
    uniform_elongation_percent: float
    fracture_strain_percent: float
    toughness_mj_m3: float


class CalculationContextResponse(BaseModel):
    """計算条件の追跡情報レスポンス."""

    youngs_modulus_fit_range: tuple[float, float]
    youngs_modulus_r_squared: float
    youngs_modulus_data_points: int
    youngs_modulus_method: str
    yield_offset_used: float
    yield_intersection_found: bool
    trim_range_applied: tuple[float, float] | None = None
    input_units: dict[str, str] = {}
    conversion_applied: list[str] = []


class AnnotationPoint(BaseModel):
    """グラフ上の注釈点."""

    label: str
    strain: float
    stress: float


class CurveDataResponse(BaseModel):
    """曲線データレスポンス."""

    strain: list[float]
    stress: list[float]
    curve_type: str
    regression_line: dict | None = None
    offset_line: dict | None = None
    annotation_points: list[AnnotationPoint] = []


class WarningResponse(BaseModel):
    """警告レスポンス."""

    metric: str
    message: str
    severity: str


class AnalysisResponse(BaseModel):
    """解析結果レスポンス.

    Attributes:
        analysis_id: 解析ID
        specimen_name: 試験片名
        results: 機械的特性の算出結果
        calculation_context: 計算条件の追跡情報
        curve_data: 曲線データ
        warnings: 警告リスト
    """

    analysis_id: str
    specimen_name: str
    results: MechanicalPropertiesResponse
    calculation_context: CalculationContextResponse
    curve_data: CurveDataResponse
    warnings: list[WarningResponse] = []


class RecalculateRequest(BaseModel):
    """再計算リクエスト.

    Attributes:
        youngs_modulus_strain_range: ヤング率算出のひずみ範囲
        yield_offset: 耐力のオフセット値
        trim_range: データトリミング範囲
    """

    youngs_modulus_strain_range: tuple[float, float] | None = None
    yield_offset: float = 0.002
    trim_range: tuple[float, float] | None = None
