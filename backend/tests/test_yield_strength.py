"""0.2%耐力算出のテスト."""

import numpy as np

from app.analysis.yield_strength import calculate_yield_strength
from app.analysis.youngs_modulus import calculate_youngs_modulus


class TestYieldStrength:
    """0.2%耐力算出のテストケース."""

    def test_mild_steel_yield(self, mild_steel_data) -> None:
        """軟鋼の0.2%耐力が妥当な範囲内か検証."""
        strain, stress = mild_steel_data

        ym_result, _ = calculate_youngs_modulus(strain, stress)

        ys_result, warnings = calculate_yield_strength(
            strain, stress,
            youngs_modulus_mpa=ym_result.slope_mpa,
            intercept_mpa=ym_result.intercept_mpa,
        )

        assert ys_result.intersection_found
        assert ys_result.value_mpa is not None
        # 軟鋼の耐力（模擬データ）: 200 ~ 500 MPa
        assert 200.0 < ys_result.value_mpa < 500.0

    def test_aluminum_yield(self, aluminum_data) -> None:
        """アルミニウム合金の0.2%耐力が妥当な範囲内か検証."""
        strain, stress = aluminum_data

        ym_result, _ = calculate_youngs_modulus(strain, stress)

        ys_result, warnings = calculate_yield_strength(
            strain, stress,
            youngs_modulus_mpa=ym_result.slope_mpa,
            intercept_mpa=ym_result.intercept_mpa,
        )

        assert ys_result.intersection_found
        assert ys_result.value_mpa is not None
        # アルミの耐力: 200 ~ 350 MPa
        assert 200.0 < ys_result.value_mpa < 350.0

    def test_no_intersection(self) -> None:
        """完全弾性データで交点が見つからない場合."""
        # 完全に線形なデータ（降伏しない）
        strain = np.linspace(0, 0.002, 100)
        stress = 200_000 * strain

        ys_result, warnings = calculate_yield_strength(
            strain, stress,
            youngs_modulus_mpa=200_000.0,
            intercept_mpa=0.0,
        )

        # 交点は見つからない（完全弾性ではオフセット直線と曲線が交差しない）
        assert not ys_result.intersection_found
        assert ys_result.value_mpa is None
        assert len(warnings) > 0

    def test_custom_offset(self, mild_steel_data) -> None:
        """カスタムオフセット値での算出."""
        strain, stress = mild_steel_data

        ym_result, _ = calculate_youngs_modulus(strain, stress)

        ys_result, _ = calculate_yield_strength(
            strain, stress,
            youngs_modulus_mpa=ym_result.slope_mpa,
            intercept_mpa=ym_result.intercept_mpa,
            offset=0.005,  # 0.5%オフセット
        )

        assert ys_result.offset_used == 0.005
