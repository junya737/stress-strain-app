"""解析サービスの統合テスト."""

from pathlib import Path

from app.schemas.analysis import AnalysisRequest
from app.schemas.dataset import ColumnMapping
from app.services.analysis_service import run_analysis
from app.services.dataset_service import upload_dataset

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestAnalysisService:
    """解析サービスの統合テストケース."""

    def test_full_analysis_flow(self) -> None:
        """CSVアップロード → 解析の一連のフロー."""
        # 1. アップロード
        content = (FIXTURES_DIR / "sample_steel.csv").read_bytes()
        dataset_resp = upload_dataset(content, "sample_steel.csv")

        assert dataset_resp.dataset_id is not None

        # 2. 解析実行
        request = AnalysisRequest(
            dataset_id=dataset_resp.dataset_id,
            specimen_name="Mild Steel Test",
            column_mapping=ColumnMapping(
                strain_column="strain",
                stress_column="stress_MPa",
            ),
        )
        response = run_analysis(request)

        # 3. 結果検証
        assert response.analysis_id is not None
        assert response.specimen_name == "Mild Steel Test"

        r = response.results
        # ヤング率: 概ね200 GPa付近
        assert r.youngs_modulus_gpa > 100.0
        # UTS: 460 MPa
        assert r.ultimate_tensile_strength_mpa == 460.0
        # 破断ひずみ: > 0
        assert r.fracture_strain_percent > 0

        # 計算条件
        ctx = response.calculation_context
        assert ctx.youngs_modulus_r_squared > 0.9
        assert ctx.youngs_modulus_method == "auto"

        # 曲線データ
        assert len(response.curve_data.strain) == 23
        assert len(response.curve_data.stress) == 23
        assert response.curve_data.curve_type == "engineering"

    def test_analysis_with_unit_conversion(self) -> None:
        """単位変換を含む解析フロー."""
        content = (FIXTURES_DIR / "sample_steel.csv").read_bytes()
        dataset_resp = upload_dataset(content, "sample_steel_pct.csv")

        request = AnalysisRequest(
            dataset_id=dataset_resp.dataset_id,
            specimen_name="Steel with MPa",
            column_mapping=ColumnMapping(
                strain_column="strain",
                stress_column="stress_MPa",
            ),
        )
        response = run_analysis(request)

        assert response.results.youngs_modulus_gpa > 0
