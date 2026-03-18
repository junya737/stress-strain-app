"""0.2%耐力算出モジュール.

オフセット法による耐力の算出を行う。
"""

import numpy as np
from numpy.typing import NDArray

from app.core.errors import AnalysisWarning
from app.domain.mechanical_props import YieldStrengthResult


def calculate_yield_strength(
    strain: NDArray[np.float64],
    stress: NDArray[np.float64],
    youngs_modulus_mpa: float,
    intercept_mpa: float,
    offset: float = 0.002,
) -> tuple[YieldStrengthResult, list[AnalysisWarning]]:
    """0.2%耐力をオフセット法で算出する.

    オフセット直線: σ = E × (ε - offset) + intercept
    この直線と応力ひずみ曲線の交点を検出する。

    Args:
        strain: ひずみ配列（無次元）
        stress: 応力配列（MPa）
        youngs_modulus_mpa: ヤング率（MPa）
        intercept_mpa: 回帰直線のy切片（MPa）
        offset: オフセット値（デフォルト0.002 = 0.2%）

    Returns:
        (YieldStrengthResult, 警告リスト) のタプル
    """
    warnings: list[AnalysisWarning] = []

    # オフセット直線の値を各ひずみ点で計算
    offset_line = youngs_modulus_mpa * (strain - offset) + intercept_mpa

    # 応力ひずみ曲線とオフセット直線の差分
    diff = stress - offset_line

    # 符号変化点を検出（正→負への変化 = 曲線がオフセット直線を下回る点）
    # 初期は曲線 < オフセット直線（diff < 0）、弾性域を超えると曲線 > オフセット直線
    # 降伏後に再び曲線 < オフセット直線になる点が交点
    sign_changes = np.where(np.diff(np.sign(diff)))[0]

    # 曲線がオフセット直線を上回った後の最初の交点を探す
    # diff > 0 の状態から diff < 0 への変化を探す
    intersection_strain: float | None = None
    intersection_stress: float | None = None

    for idx in sign_changes:
        # diff[idx] > 0 かつ diff[idx+1] <= 0 の交点（上から下への交差）
        if diff[idx] > 0 and diff[idx + 1] <= 0:
            # 線形補間で正確な交点を算出
            t = diff[idx] / (diff[idx] - diff[idx + 1])
            intersection_strain = float(
                strain[idx] + t * (strain[idx + 1] - strain[idx])
            )
            intersection_stress = float(
                stress[idx] + t * (stress[idx + 1] - stress[idx])
            )
            break

    if intersection_strain is None:
        # 別のアプローチ: diff < 0 → diff > 0 → diff < 0 のパターンを探す
        # まず diff > 0 になる最初の点以降で、diff < 0 になる点を探す
        positive_mask = diff > 0
        if np.any(positive_mask):
            first_positive = np.argmax(positive_mask)
            remaining_diff = diff[first_positive:]
            negative_after = np.where(remaining_diff < 0)[0]
            if len(negative_after) > 0:
                cross_idx = first_positive + negative_after[0] - 1
                if cross_idx >= 0 and cross_idx < len(strain) - 1:
                    t = diff[cross_idx] / (diff[cross_idx] - diff[cross_idx + 1])
                    intersection_strain = float(
                        strain[cross_idx]
                        + t * (strain[cross_idx + 1] - strain[cross_idx])
                    )
                    intersection_stress = float(
                        stress[cross_idx]
                        + t * (stress[cross_idx + 1] - stress[cross_idx])
                    )

    if intersection_strain is None:
        warnings.append(
            AnalysisWarning(
                metric="yield_strength",
                message=(
                    "Offset line and stress-strain curve do not intersect. "
                    "Yield strength could not be determined."
                ),
                severity="warning",
            )
        )
        return (
            YieldStrengthResult(
                value_mpa=None,
                offset_used=offset,
                intersection_found=False,
            ),
            warnings,
        )

    return (
        YieldStrengthResult(
            value_mpa=intersection_stress,
            offset_used=offset,
            intersection_found=True,
        ),
        warnings,
    )
