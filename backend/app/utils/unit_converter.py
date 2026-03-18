"""単位変換ユーティリティ."""

import numpy as np
from numpy.typing import NDArray

from app.domain.enums import StrainUnit, StressUnit


def convert_strain_to_dimensionless(
    strain: NDArray[np.float64],
    unit: StrainUnit,
) -> NDArray[np.float64]:
    """ひずみを無次元に変換する.

    Args:
        strain: ひずみ配列
        unit: 入力の単位

    Returns:
        無次元ひずみ配列
    """
    if unit == StrainUnit.DIMENSIONLESS:
        return strain
    elif unit == StrainUnit.PERCENT:
        return strain / 100.0
    elif unit == StrainUnit.MICROSTRAIN:
        return strain / 1_000_000.0
    else:
        assert False, f"Unknown strain unit: {unit}"


def convert_stress_to_mpa(
    stress: NDArray[np.float64],
    unit: StressUnit,
) -> NDArray[np.float64]:
    """応力をMPaに変換する.

    Args:
        stress: 応力配列
        unit: 入力の単位

    Returns:
        MPa単位の応力配列
    """
    if unit == StressUnit.MPA:
        return stress
    elif unit == StressUnit.GPA:
        return stress * 1000.0
    elif unit == StressUnit.KSI:
        return stress * 6.89476
    else:
        assert False, f"Unknown stress unit: {unit}"
