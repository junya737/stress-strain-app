"""靱性（曲線下面積）算出モジュール."""

import numpy as np
from numpy.typing import NDArray


def calculate_toughness(
    strain: NDArray[np.float64],
    stress: NDArray[np.float64],
    end_index: int | None = None,
) -> float:
    """応力ひずみ曲線の下面積（靱性）を算出する.

    台形法で面積を計算する。ひずみが無次元、応力がMPaの場合、
    結果の単位はMJ/m³（= MPa）。

    Args:
        strain: ひずみ配列（無次元）
        stress: 応力配列（MPa）
        end_index: 積分の終了インデックス（Noneの場合は全範囲）

    Returns:
        靱性値（MJ/m³）
    """
    if end_index is not None:
        strain = strain[: end_index + 1]
        stress = stress[: end_index + 1]

    return float(np.trapezoid(stress, strain))
