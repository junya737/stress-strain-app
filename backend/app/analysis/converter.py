"""工学⇔真応力ひずみ変換モジュール."""

import numpy as np
from numpy.typing import NDArray


def engineering_to_true(
    eng_strain: NDArray[np.float64],
    eng_stress: NDArray[np.float64],
    uts_index: int | None = None,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """工学応力ひずみから真応力ひずみに変換する.

    真ひずみ: ε_true = ln(1 + ε_eng)
    真応力: σ_true = σ_eng × (1 + ε_eng)

    UTSを超えるとネッキングにより変換式が不正確になるため、
    uts_indexが指定された場合はそこまでに制限する。

    Args:
        eng_strain: 工学ひずみ配列（無次元）
        eng_stress: 工学応力配列（MPa）
        uts_index: UTSのインデックス。指定時はここまでに制限

    Returns:
        (真ひずみ, 真応力) のタプル
    """
    if uts_index is not None:
        eng_strain = eng_strain[: uts_index + 1]
        eng_stress = eng_stress[: uts_index + 1]

    true_strain = np.log(1.0 + eng_strain)
    true_stress = eng_stress * (1.0 + eng_strain)

    return true_strain, true_stress
