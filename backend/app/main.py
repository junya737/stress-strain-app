"""FastAPIアプリケーション エントリポイント."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import analyses, datasets, exports
from app.core.config import AppConfig

config = AppConfig()

app = FastAPI(
    title="Stress-Strain Analysis API",
    version="0.1.0",
    description="材料試験データの応力ひずみ解析API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(config.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(datasets.router, prefix="/api/v1")
app.include_router(analyses.router, prefix="/api/v1")
app.include_router(exports.router, prefix="/api/v1")


@app.get("/api/v1/health")
def health_check() -> dict[str, str]:
    """ヘルスチェック."""
    return {"status": "ok"}
