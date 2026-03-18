"""UTS（引張強さ）算出モジュール."""

import numpy as np
from numpy.typing import NDArray

from app.domain.mechanical_props import UTSResult


def calculate_uts(
    strain: NDArray[np.float64],
    stress: NDArray[np.float64],
    smoothing_window: int = 5,
) -> UTSResult:
    """引張強さ（UTS）を算出する.

    応力の最大値をUTSとする。データ点が1000を超える場合は
    移動平均で平滑化してからピークを検出する。

    Args:
        strain: ひずみ配列（無次元）
        stress: 応力配列（MPa）
        smoothing_window: 平滑化の移動平均窓幅

    Returns:
        UTSResult
    """
    if len(stress) > 1000 and smoothing_window > 1:
        # 移動平均で平滑化
        kernel = np.ones(smoothing_window) / smoothing_window
        smoothed = np.convolve(stress, kernel, mode="same")
        uts_index = int(np.argmax(smoothed))
    else:
        uts_index = int(np.argmax(stress))

    return UTSResult(
        value_mpa=float(stress[uts_index]),
        strain_at_uts=float(strain[uts_index]),
        index=uts_index,
    )
