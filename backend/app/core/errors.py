"""バリデーションエラー・解析警告の型定義."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationError:
    """バリデーションエラー.

    CSVパース、列マッピング、単位不整合などの入力検証エラーを表す。

    Attributes:
        field: エラーが発生したフィールド名
        message: エラーメッセージ
        error_type: エラー種別
    """

    field: str
    message: str
    error_type: str  # "missing_column" | "unit_mismatch" | "empty_data" | ...


@dataclass(frozen=True)
class AnalysisWarning:
    """解析品質の警告.

    解析は完了したが品質に問題がある場合の警告を表す。

    Attributes:
        metric: 警告対象の指標名
        message: 警告メッセージ
        severity: 重要度
    """

    metric: str
    message: str
    severity: str  # "info" | "warning" | "critical"
