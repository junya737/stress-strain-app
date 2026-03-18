"""データセット（CSVアップロード）APIルーター."""

from fastapi import APIRouter, HTTPException, UploadFile

from app.schemas.dataset import DatasetResponse
from app.services.dataset_service import get_store, upload_dataset

router = APIRouter(tags=["datasets"])


@router.post("/datasets", response_model=DatasetResponse)
async def create_dataset(file: UploadFile) -> DatasetResponse:
    """CSVファイルをアップロードし、メタデータを返す.

    Args:
        file: アップロードされたCSVファイル

    Returns:
        DatasetResponse
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    return upload_dataset(content, file.filename)


@router.get("/datasets/{dataset_id}/preview")
async def get_dataset_preview(dataset_id: str) -> dict:
    """データセットのプレビューを返す.

    Args:
        dataset_id: データセットID

    Returns:
        プレビュー情報
    """
    store = get_store()
    if dataset_id not in store.datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")

    parsed = store.datasets[dataset_id]
    preview = parsed.df.head(10).to_dict(orient="records")
    return {
        "dataset_id": dataset_id,
        "columns": parsed.columns,
        "row_count": parsed.row_count,
        "preview": preview,
    }
