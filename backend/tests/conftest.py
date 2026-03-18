"""テスト用のフィクスチャ定義."""

import numpy as np
import pytest
from numpy.typing import NDArray


@pytest.fixture
def mild_steel_data() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """軟鋼の応力ひずみデータ（模擬）.

    E ≈ 200 GPa, UTS ≈ 450 MPa, 0.2%耐力 ≈ 250 MPa
    破断ひずみ ≈ 25%

    Returns:
        (ひずみ, 応力) のタプル
    """
    # 弾性域: 0 ~ 0.15% (E = 200 GPa = 200,000 MPa)
    E = 200_000.0  # MPa
    elastic_strain = np.linspace(0, 0.0015, 100)
    elastic_stress = E * elastic_strain

    # 降伏〜加工硬化域: 0.15% ~ 15%
    plastic_strain = np.linspace(0.0015, 0.15, 500)
    # Hollomon式近似: σ = K * ε_p^n + σ_y
    sigma_y = 300.0  # MPa
    K = 600.0
    n = 0.25
    eps_p = plastic_strain - sigma_y / E
    eps_p = np.maximum(eps_p, 0)
    plastic_stress = sigma_y + K * (eps_p**n)
    # UTSまで上昇（約450 MPa）
    plastic_stress = np.minimum(plastic_stress, 460.0)

    # ネッキング〜破断: 15% ~ 25%
    fracture_strain = np.linspace(0.15, 0.25, 100)
    uts = plastic_stress[-1]
    fracture_stress = uts * np.exp(-3.0 * (fracture_strain - 0.15))

    strain = np.concatenate([elastic_strain, plastic_strain, fracture_strain])
    stress = np.concatenate([elastic_stress, plastic_stress, fracture_stress])

    return strain, stress


@pytest.fixture
def aluminum_data() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """アルミニウム合金の応力ひずみデータ（模擬）.

    E ≈ 70 GPa, UTS ≈ 310 MPa, 0.2%耐力 ≈ 275 MPa
    破断ひずみ ≈ 12%

    Returns:
        (ひずみ, 応力) のタプル
    """
    E = 70_000.0  # MPa
    elastic_strain = np.linspace(0, 0.004, 80)
    elastic_stress = E * elastic_strain

    plastic_strain = np.linspace(0.004, 0.08, 300)
    sigma_y = 275.0
    K = 200.0
    n = 0.15
    eps_p = plastic_strain - sigma_y / E
    eps_p = np.maximum(eps_p, 0)
    plastic_stress = sigma_y + K * (eps_p**n)
    plastic_stress = np.minimum(plastic_stress, 315.0)

    fracture_strain = np.linspace(0.08, 0.12, 50)
    uts = plastic_stress[-1]
    fracture_stress = uts * np.exp(-5.0 * (fracture_strain - 0.08))

    strain = np.concatenate([elastic_strain, plastic_strain, fracture_strain])
    stress = np.concatenate([elastic_stress, plastic_stress, fracture_stress])

    return strain, stress
