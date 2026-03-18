"""CSVパーサーのテスト."""

from pathlib import Path

import numpy as np

from app.io.csv_parser import extract_arrays, parse_csv

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestParseCSV:
    """CSVパースのテストケース."""

    def test_parse_steel_csv(self) -> None:
        """軟鋼CSVのパースと列推定."""
        content = (FIXTURES_DIR / "sample_steel.csv").read_bytes()
        parsed = parse_csv(content, "sample_steel.csv")

        assert parsed.row_count == 23
        assert "strain" in parsed.columns
        assert "stress_MPa" in parsed.columns
        assert parsed.suggested_strain_col == "strain"
        assert parsed.suggested_stress_col == "stress_MPa"

    def test_parse_load_disp_csv(self) -> None:
        """荷重-変位CSVのパースと列推定."""
        content = (FIXTURES_DIR / "sample_load_disp.csv").read_bytes()
        parsed = parse_csv(content, "sample_load_disp.csv")

        assert parsed.row_count == 13
        assert parsed.suggested_disp_col == "displacement_mm"
        assert parsed.suggested_load_col == "load_N"

    def test_detect_encoding_utf8(self) -> None:
        """UTF-8エンコーディングの検出."""
        content = "strain,stress\n0.001,200\n".encode("utf-8")
        parsed = parse_csv(content)

        assert parsed.encoding == "utf-8"

    def test_detect_delimiter_tab(self) -> None:
        """タブ区切りの検出."""
        content = "strain\tstress\n0.001\t200\n0.002\t400\n".encode("utf-8")
        parsed = parse_csv(content)

        assert parsed.delimiter == "\t"
        assert parsed.row_count == 2


class TestExtractArrays:
    """配列抽出のテストケース."""

    def test_extract_stress_strain(self) -> None:
        """応力ひずみ列から配列を抽出."""
        content = (FIXTURES_DIR / "sample_steel.csv").read_bytes()
        parsed = parse_csv(content)

        strain, stress = extract_arrays(
            parsed.df,
            strain_col="strain",
            stress_col="stress_MPa",
        )

        assert len(strain) == 23
        assert len(stress) == 23
        assert strain[0] == 0.0
        assert stress[-1] == 350.0  # 最終行

    def test_extract_from_load_displacement(self) -> None:
        """荷重-変位から応力ひずみを算出."""
        content = (FIXTURES_DIR / "sample_load_disp.csv").read_bytes()
        parsed = parse_csv(content)

        strain, stress = extract_arrays(
            parsed.df,
            strain_col="displacement_mm",  # 代替: displacement使用
            displacement_col="displacement_mm",
            load_col="load_N",
            cross_section_area=10.0,  # mm²
            gauge_length=50.0,  # mm
        )

        assert len(strain) == 13
        # 最初の変位=0 → ひずみ=0
        assert strain[0] == 0.0
        # 荷重=500 / 面積=10 → 応力=50 MPa
        np.testing.assert_almost_equal(stress[1], 50.0)
