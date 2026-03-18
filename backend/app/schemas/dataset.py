"""データセット関連のPydanticスキーマ（API境界）."""

from pydantic import BaseModel

from app.domain.enums import StrainUnit, StressUnit


class ColumnMapping(BaseModel):
    """列マッピング + 試験片パラメータ.

    Attributes:
        strain_column: ひずみ列名
        stress_column: 応力列名（応力データがある場合）
        load_column: 荷重列名（荷重データがある場合）
        displacement_column: 変位列名（変位データがある場合）
        cross_section_area: 断面積（mm²）。荷重→応力変換時に必要
        gauge_length: 標点距離（mm）。変位→ひずみ変換時に必要
        strain_unit: ひずみの単位
        stress_unit: 応力の単位
    """

    strain_column: str
    stress_column: str | None = None
    load_column: str | None = None
    displacement_column: str | None = None
    cross_section_area: float | None = None
    gauge_length: float | None = None
    strain_unit: StrainUnit = StrainUnit.DIMENSIONLESS
    stress_unit: StressUnit = StressUnit.MPA


class DatasetResponse(BaseModel):
    """CSVアップロードレスポンス.

    Attributes:
        dataset_id: UUID
        filename: アップロードファイル名
        detected_columns: 検出された列名リスト
        row_count: データ行数
        preview: 先頭5行のプレビュー
        suggested_mapping: 自動推定された列マッピング
        detected_encoding: 検出されたエンコーディング
        detected_delimiter: 検出された区切り文字
    """

    dataset_id: str
    filename: str
    detected_columns: list[str]
    row_count: int
    preview: list[dict]
    suggested_mapping: ColumnMapping | None = None
    detected_encoding: str = "utf-8"
    detected_delimiter: str = ","
