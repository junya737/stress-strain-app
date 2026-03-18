"""アプリケーション設定."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """アプリケーション設定.

    Attributes:
        host: サーバーホスト
        port: サーバーポート
        cors_origins: CORSで許可するオリジン
        max_upload_size_mb: アップロードファイルの最大サイズ(MB)
        upload_dir: アップロードファイルの一時保存先
    """

    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: tuple[str, ...] = ("http://localhost:3000",)
    max_upload_size_mb: int = 50
    upload_dir: str = "/tmp/stress-strain-uploads"
