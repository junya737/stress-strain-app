"""機械的特性の結果型."""

from dataclasses import dataclass, field

from app.core.errors import AnalysisWarning


@dataclass(frozen=True)
class YoungsModulusResult:
    """ヤング率算出結果.

    Attributes:
        value_gpa: ヤング率（GPa）
        r_squared: 回帰のR²値
        fit_range: 回帰に使用したひずみ範囲（開始, 終了）
        data_points: 回帰に使用したデータ点数
        method: 算出方法（"auto" | "manual"）
        slope_mpa: 回帰直線の傾き（MPa）
        intercept_mpa: 回帰直線のy切片（MPa）
    """

    value_gpa: float
    r_squared: float
    fit_range: tuple[float, float]
    data_points: int
    method: str
    slope_mpa: float
    intercept_mpa: float


@dataclass(frozen=True)
class YieldStrengthResult:
    """0.2%耐力算出結果.

    Attributes:
        value_mpa: 耐力値（MPa）。交点未検出時はNone
        offset_used: 使用したオフセット値
        intersection_found: 交点が検出されたか
    """

    value_mpa: float | None
    offset_used: float
    intersection_found: bool


@dataclass(frozen=True)
class UTSResult:
    """引張強さ算出結果.

    Attributes:
        value_mpa: UTS（MPa）
        strain_at_uts: UTS時のひずみ
        index: UTSのデータ点インデックス
    """

    value_mpa: float
    strain_at_uts: float
    index: int


@dataclass(frozen=True)
class FractureResult:
    """破断点算出結果.

    Attributes:
        strain: 破断ひずみ
        stress_mpa: 破断応力（MPa）
        index: 破断点のデータ点インデックス
    """

    strain: float
    stress_mpa: float
    index: int


@dataclass(frozen=True)
class MechanicalProperties:
    """全機械的特性の集約結果.

    Attributes:
        youngs_modulus: ヤング率結果
        yield_strength: 0.2%耐力結果
        uts: UTS結果
        fracture: 破断点結果
        toughness_mj_m3: 靱性（MJ/m³）
        warnings: 解析中に発生した警告リスト
    """

    youngs_modulus: YoungsModulusResult
    yield_strength: YieldStrengthResult
    uts: UTSResult
    fracture: FractureResult
    toughness_mj_m3: float
    warnings: list[AnalysisWarning] = field(default_factory=list)
