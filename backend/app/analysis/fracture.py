"""破断点検出モジュール."""

import numpy as np
from numpy.typing import NDArray

from app.domain.mechanical_props import FractureResult


def detect_fracture(
    strain: NDArray[np.float64],
    stress: NDArray[np.float64],
    uts_index: int,
    stress_drop_ratio: float = 0.5,
) -> FractureResult:
    """破断点を検出する.

    UTS以降で応力が急激に低下する点を破断点とする。
    検出できない場合はデータ最終点を使用する。

    Args:
        strain: ひずみ配列（無次元）
        stress: 応力配列（MPa）
        uts_index: UTSのデータ点インデックス
        stress_drop_ratio: UTS応力に対する応力低下の閾値比率

    Returns:
        FractureResult
    """
    uts_stress = stress[uts_index]

    # UTS以降のデータを探索
    post_uts = stress[uts_index:]

    if len(post_uts) <= 1:
        # UTS以降のデータがない場合は最終点
        idx = len(strain) - 1
        return FractureResult(
            strain=float(strain[idx]),
            stress_mpa=float(stress[idx]),
            index=idx,
        )

    # 応力がUTSからstress_drop_ratio以上低下した点を検出
    threshold = uts_stress * (1.0 - stress_drop_ratio)
    below_threshold = np.where(post_uts < threshold)[0]

    if len(below_threshold) > 0:
        fracture_relative_idx = below_threshold[0]
        fracture_idx = uts_index + fracture_relative_idx
    else:
        # 閾値以下にならない場合はデータ最終点
        fracture_idx = len(strain) - 1

    return FractureResult(
        strain=float(strain[fracture_idx]),
        stress_mpa=float(stress[fracture_idx]),
        index=fracture_idx,
    )
