"""データセットサービス.

CSVの取込・前処理フローを調停する。
"""

import uuid
from dataclasses import dataclass, field

import pandas as pd

from app.io.csv_parser import ParsedCSV, parse_csv
from app.schemas.dataset import ColumnMapping, DatasetResponse


@dataclass
class DatasetStore:
    """インメモリのデータセット保管庫.

    MVPではメモリ上にDataFrameを保持する。
    将来的にはDBやファイルストレージに置き換え可能。

    Attributes:
        datasets: データセットIDとパース結果のマッピング
    """

    datasets: dict[str, ParsedCSV] = field(default_factory=dict)


# シングルトン（MVP用）
_store = DatasetStore()


def get_store() -> DatasetStore:
    """データセットストアを取得する."""
    return _store


def upload_dataset(content: bytes, filename: str) -> DatasetResponse:
    """CSVファイルをアップロードし、メタデータを返す.

    Args:
        content: CSVファイルのバイト列
        filename: ファイル名

    Returns:
        DatasetResponse
    """
    dataset_id = str(uuid.uuid4())
    parsed = parse_csv(content, filename)

    _store.datasets[dataset_id] = parsed

    # 推定マッピングの構築
    suggested_mapping: ColumnMapping | None = None
    if parsed.suggested_strain_col:
        suggested_mapping = ColumnMapping(
            strain_column=parsed.suggested_strain_col,
            stress_column=parsed.suggested_stress_col,
            load_column=parsed.suggested_load_col,
            displacement_column=parsed.suggested_disp_col,
        )

    # プレビュー（先頭5行）
    preview_df = parsed.df.head(5)
    preview = preview_df.to_dict(orient="records")

    return DatasetResponse(
        dataset_id=dataset_id,
        filename=filename,
        detected_columns=parsed.columns,
        row_count=parsed.row_count,
        preview=preview,
        suggested_mapping=suggested_mapping,
        detected_encoding=parsed.encoding,
        detected_delimiter=parsed.delimiter,
    )


def get_dataframe(dataset_id: str) -> pd.DataFrame:
    """データセットIDからDataFrameを取得する.

    Args:
        dataset_id: データセットID

    Returns:
        DataFrame
    """
    assert dataset_id in _store.datasets, (
        f"Dataset '{dataset_id}' not found"
    )
    return _store.datasets[dataset_id].df
