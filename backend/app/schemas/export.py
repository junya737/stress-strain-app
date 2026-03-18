"""エクスポート関連のPydanticスキーマ."""

from pydantic import BaseModel


class ExportImageRequest(BaseModel):
    """画像エクスポートリクエスト.

    Attributes:
        format: 画像形式（"png" | "svg"）
        width_mm: 幅（mm）。論文用プリセット対応
        dpi: 解像度
    """

    format: str = "png"
    width_mm: float = 170.0
    dpi: int = 300
