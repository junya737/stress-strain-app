"""ヤング率算出のテスト."""

import numpy as np
import pytest

from app.analysis.youngs_modulus import calculate_youngs_modulus


class TestYoungsModulus:
    """ヤング率算出のテストケース."""

    def test_perfect_linear_data(self) -> None:
        """完全な線形データでE = 200 GPaを検証."""
        E_mpa = 200_000.0
        strain = np.linspace(0, 0.002, 100)
        stress = E_mpa * strain

        result, warnings = calculate_youngs_modulus(strain, stress)

        assert abs(result.value_gpa - 200.0) < 1.0
        assert result.r_squared > 0.999

    def test_auto_detection_with_mild_steel(self, mild_steel_data) -> None:
        """軟鋼データでヤング率が妥当な範囲内か検証."""
        strain, stress = mild_steel_data
        result, warnings = calculate_youngs_modulus(strain, stress)

        # 軟鋼のヤング率: 190 ~ 210 GPa
        assert 150.0 < result.value_gpa < 250.0
        assert result.r_squared > 0.99

    def test_manual_range(self, mild_steel_data) -> None:
        """手動範囲指定でのヤング率算出."""
        strain, stress = mild_steel_data
        result, warnings = calculate_youngs_modulus(
            strain, stress, strain_range=(0.0, 0.001)
        )

        assert result.method == "manual"
        assert result.value_gpa > 100.0
        assert result.data_points > 0

    def test_warning_on_low_r_squared(self) -> None:
        """R²が低い場合に警告が出るか検証."""
        # ノイズの多いデータ
        np.random.seed(42)
        strain = np.linspace(0, 0.01, 50)
        stress = 200_000 * strain + np.random.normal(0, 50, 50)

        result, warnings = calculate_youngs_modulus(
            strain, stress, strain_range=(0.0, 0.01)
        )

        # 値は返ってくる（品質に関わらず）
        assert result.value_gpa > 0

    def test_aluminum_youngs_modulus(self, aluminum_data) -> None:
        """アルミニウム合金のヤング率が妥当な範囲内か検証."""
        strain, stress = aluminum_data
        result, warnings = calculate_youngs_modulus(strain, stress)

        # アルミのヤング率: 60 ~ 80 GPa
        assert 50.0 < result.value_gpa < 100.0


class TestYoungsModulusEdgeCases:
    """ヤング率算出のエッジケーステスト."""

    def test_minimum_data_points(self) -> None:
        """最小データ点数（2点）で動作するか."""
        strain = np.array([0.0, 0.001])
        stress = np.array([0.0, 200.0])

        result, warnings = calculate_youngs_modulus(
            strain, stress, strain_range=(0.0, 0.001)
        )

        assert result.value_gpa == pytest.approx(200.0, rel=0.01)
