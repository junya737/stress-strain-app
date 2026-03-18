"""列挙型定義."""

from enum import Enum


class StrainUnit(str, Enum):
    """ひずみの単位."""

    DIMENSIONLESS = "dimensionless"
    PERCENT = "percent"
    MICROSTRAIN = "microstrain"


class StressUnit(str, Enum):
    """応力の単位."""

    MPA = "MPa"
    GPA = "GPa"
    KSI = "ksi"


class CurveType(str, Enum):
    """応力ひずみ曲線の種別."""

    ENGINEERING = "engineering"
    TRUE = "true"
