"""解析APIルーター."""

from fastapi import APIRouter, HTTPException

from app.schemas.analysis import (
    AnalysisRequest,
    AnalysisResponse,
    RecalculateRequest,
)
from app.services.analysis_service import (
    get_analysis,
    recalculate_analysis,
    run_analysis,
)

router = APIRouter(tags=["analyses"])


@router.post("/analyses", response_model=AnalysisResponse)
async def create_analysis(request: AnalysisRequest) -> AnalysisResponse:
    """解析を実行する.

    Args:
        request: 解析リクエスト

    Returns:
        AnalysisResponse
    """
    return run_analysis(request)


@router.get("/analyses/{analysis_id}", response_model=AnalysisResponse)
async def read_analysis(analysis_id: str) -> AnalysisResponse:
    """解析結果を取得する.

    Args:
        analysis_id: 解析ID

    Returns:
        AnalysisResponse
    """
    try:
        return get_analysis(analysis_id)
    except AssertionError:
        raise HTTPException(status_code=404, detail="Analysis not found")


@router.post(
    "/analyses/{analysis_id}/recalculate",
    response_model=AnalysisResponse,
)
async def recalculate(
    analysis_id: str,
    request: RecalculateRequest,
) -> AnalysisResponse:
    """手動補正後の再計算.

    Args:
        analysis_id: 解析ID
        request: 再計算リクエスト

    Returns:
        更新されたAnalysisResponse
    """
    try:
        return recalculate_analysis(analysis_id, request)
    except AssertionError:
        raise HTTPException(status_code=404, detail="Analysis not found")
