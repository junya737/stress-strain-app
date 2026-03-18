"""ヤング率算出モジュール.

移動窓回帰 + R²選択による自動推定と、手動範囲指定の両方に対応する。
"""

import numpy as np
from numpy.typing import NDArray

from app.core.errors import AnalysisWarning
from app.domain.mechanical_props import YoungsModulusResult

# 品質基準
_R_SQUARED_THRESHOLD = 0.999
_MIN_DATA_POINTS = 10


def calculate_youngs_modulus(
    strain: NDArray[np.float64],
    stress: NDArray[np.float64],
    strain_range: tuple[float, float] | None = None,
    window_fraction: float = 0.05,
    min_window_points: int = 20,
) -> tuple[YoungsModulusResult, list[AnalysisWarning]]:
    """ヤング率を算出する.

    移動窓回帰で線形域を自動検出し、最もR²が高い区間の傾きをヤング率とする。
    strain_rangeが指定された場合はその範囲で回帰を行う。

    Args:
        strain: ひずみ配列（無次元）
        stress: 応力配列（MPa）
        strain_range: 手動指定のひずみ範囲。Noneの場合は自動推定
        window_fraction: 移動窓のデータ全体に対する比率
        min_window_points: 移動窓の最小データ点数

    Returns:
        (YoungsModulusResult, 警告リスト) のタプル
    """
    warnings: list[AnalysisWarning] = []

    if strain_range is not None:
        return _fit_in_range(strain, stress, strain_range, "manual", warnings)

    return _auto_detect(
        strain, stress, window_fraction, min_window_points, warnings
    )


def _fit_in_range(
    strain: NDArray[np.float64],
    stress: NDArray[np.float64],
    strain_range: tuple[float, float],
    method: str,
    warnings: list[AnalysisWarning],
) -> tuple[YoungsModulusResult, list[AnalysisWarning]]:
    """指定範囲で線形回帰を実行する."""
    mask = (strain >= strain_range[0]) & (strain <= strain_range[1])
    s_fit = strain[mask]
    st_fit = stress[mask]

    assert len(s_fit) >= 2, (
        f"Not enough data points in range {strain_range}: {len(s_fit)}"
    )

    slope, intercept, r_squared = _linear_regression(s_fit, st_fit)

    if r_squared < _R_SQUARED_THRESHOLD:
        warnings.append(
            AnalysisWarning(
                metric="youngs_modulus",
                message=(
                    f"R² = {r_squared:.6f} is below threshold "
                    f"{_R_SQUARED_THRESHOLD}. Linear fit may not be reliable."
                ),
                severity="warning",
            )
        )

    if len(s_fit) < _MIN_DATA_POINTS:
        warnings.append(
            AnalysisWarning(
                metric="youngs_modulus",
                message=(
                    f"Only {len(s_fit)} data points used for regression. "
                    f"Recommend at least {_MIN_DATA_POINTS}."
                ),
                severity="info",
            )
        )

    result = YoungsModulusResult(
        value_gpa=slope / 1000.0,
        r_squared=r_squared,
        fit_range=(float(s_fit[0]), float(s_fit[-1])),
        data_points=len(s_fit),
        method=method,
        slope_mpa=slope,
        intercept_mpa=intercept,
    )
    return result, warnings


def _auto_detect(
    strain: NDArray[np.float64],
    stress: NDArray[np.float64],
    window_fraction: float,
    min_window_points: int,
    warnings: list[AnalysisWarning],
) -> tuple[YoungsModulusResult, list[AnalysisWarning]]:
    """移動窓回帰で線形域を自動検出する."""
    n = len(strain)
    # データ点が少ない場合は窓サイズを適応的に縮小
    effective_min = min(min_window_points, max(3, n // 3))
    window_size = max(effective_min, int(n * window_fraction))

    # 探索範囲: 全データの前半部分（弾性域は前半に存在する）
    search_limit = min(n, max(int(n * 0.5), window_size + 1))

    best_r_squared = -1.0
    best_start = 0
    best_end = window_size

    for start in range(0, search_limit - window_size + 1):
        end = start + window_size
        s_win = strain[start:end]
        st_win = stress[start:end]

        # ひずみが単調でないウィンドウはスキップ
        if s_win[-1] <= s_win[0]:
            continue

        _, _, r_sq = _linear_regression(s_win, st_win)

        if r_sq > best_r_squared:
            best_r_squared = r_sq
            best_start = start
            best_end = end

    # 最良窓で回帰
    best_range = (float(strain[best_start]), float(strain[best_end - 1]))
    result, fit_warnings = _fit_in_range(
        strain, stress, best_range, "auto", warnings
    )
    return result, fit_warnings


def _linear_regression(
    x: NDArray[np.float64],
    y: NDArray[np.float64],
) -> tuple[float, float, float]:
    """最小二乗法による線形回帰.

    Args:
        x: 説明変数
        y: 目的変数

    Returns:
        (傾き, y切片, R²) のタプル
    """
    n = len(x)
    assert n >= 2, "Need at least 2 points for regression"

    x_mean = np.mean(x)
    y_mean = np.mean(y)

    ss_xx = np.sum((x - x_mean) ** 2)
    ss_yy = np.sum((y - y_mean) ** 2)
    ss_xy = np.sum((x - x_mean) * (y - y_mean))

    # ほぼゼロの分散 → R²=0
    if ss_xx < 1e-30:
        return 0.0, float(y_mean), 0.0

    slope = float(ss_xy / ss_xx)
    intercept = float(y_mean - slope * x_mean)

    if ss_yy < 1e-30:
        r_squared = 1.0 if ss_xx < 1e-30 else 0.0
    else:
        r_squared = float((ss_xy**2) / (ss_xx * ss_yy))

    return slope, intercept, r_squared
