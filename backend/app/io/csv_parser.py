"""CSVパース・列検出・エンコーディング推定モジュール."""

import io
import re
from dataclasses import dataclass

import numpy as np
import pandas as pd
from numpy.typing import NDArray


# 列名の自動推定用パターン
_STRAIN_PATTERNS = [
    re.compile(r"strain", re.IGNORECASE),
    re.compile(r"ひずみ", re.IGNORECASE),
    re.compile(r"歪み?", re.IGNORECASE),
    re.compile(r"epsilon", re.IGNORECASE),
    re.compile(r"ε", re.IGNORECASE),
    re.compile(r"eng[._\s-]?strain", re.IGNORECASE),
]

_STRESS_PATTERNS = [
    re.compile(r"stress", re.IGNORECASE),
    re.compile(r"応力", re.IGNORECASE),
    re.compile(r"sigma", re.IGNORECASE),
    re.compile(r"σ", re.IGNORECASE),
    re.compile(r"eng[._\s-]?stress", re.IGNORECASE),
]

_LOAD_PATTERNS = [
    re.compile(r"load", re.IGNORECASE),
    re.compile(r"force", re.IGNORECASE),
    re.compile(r"荷重", re.IGNORECASE),
]

_DISPLACEMENT_PATTERNS = [
    re.compile(r"disp", re.IGNORECASE),
    re.compile(r"displacement", re.IGNORECASE),
    re.compile(r"変位", re.IGNORECASE),
    re.compile(r"extension", re.IGNORECASE),
    re.compile(r"elongation", re.IGNORECASE),
]


@dataclass
class ParsedCSV:
    """パース結果.

    Attributes:
        df: データフレーム
        columns: 列名リスト
        row_count: データ行数
        encoding: 検出されたエンコーディング
        delimiter: 検出された区切り文字
        suggested_strain_col: 推定されたひずみ列名
        suggested_stress_col: 推定された応力列名
        suggested_load_col: 推定された荷重列名
        suggested_disp_col: 推定された変位列名
    """

    df: pd.DataFrame
    columns: list[str]
    row_count: int
    encoding: str
    delimiter: str
    suggested_strain_col: str | None
    suggested_stress_col: str | None
    suggested_load_col: str | None
    suggested_disp_col: str | None


def parse_csv(content: bytes, filename: str = "") -> ParsedCSV:
    """CSVバイト列をパースする.

    エンコーディングと区切り文字を自動検出し、列名を推定する。

    Args:
        content: CSVファイルのバイト列
        filename: ファイル名（ログ用）

    Returns:
        ParsedCSV
    """
    encoding = _detect_encoding(content)
    text = content.decode(encoding)
    delimiter = _detect_delimiter(text)

    df = pd.read_csv(io.StringIO(text), sep=delimiter)

    # 数値列のみ抽出
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    columns = df.columns.tolist()

    return ParsedCSV(
        df=df,
        columns=columns,
        row_count=len(df),
        encoding=encoding,
        delimiter=delimiter,
        suggested_strain_col=_find_matching_column(columns, _STRAIN_PATTERNS),
        suggested_stress_col=_find_matching_column(columns, _STRESS_PATTERNS),
        suggested_load_col=_find_matching_column(columns, _LOAD_PATTERNS),
        suggested_disp_col=_find_matching_column(
            columns, _DISPLACEMENT_PATTERNS
        ),
    )


def extract_arrays(
    df: pd.DataFrame,
    strain_col: str,
    stress_col: str | None = None,
    load_col: str | None = None,
    displacement_col: str | None = None,
    cross_section_area: float | None = None,
    gauge_length: float | None = None,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """DataFrameから応力ひずみ配列を抽出する.

    応力列がない場合は荷重列と断面積から計算する。
    ひずみ列がない場合は変位列と標点距離から計算する。

    Args:
        df: データフレーム
        strain_col: ひずみ列名
        stress_col: 応力列名
        load_col: 荷重列名
        displacement_col: 変位列名
        cross_section_area: 断面積（mm²）
        gauge_length: 標点距離（mm）

    Returns:
        (ひずみ配列, 応力配列) のタプル
    """
    # ひずみの取得
    if strain_col in df.columns:
        strain = df[strain_col].to_numpy(dtype=np.float64)
    elif displacement_col and displacement_col in df.columns:
        assert gauge_length is not None and gauge_length > 0, (
            "gauge_length is required for displacement-to-strain conversion"
        )
        disp = df[displacement_col].to_numpy(dtype=np.float64)
        strain = disp / gauge_length
    else:
        assert False, f"Strain column '{strain_col}' not found in data"

    # 応力の取得
    if stress_col and stress_col in df.columns:
        stress = df[stress_col].to_numpy(dtype=np.float64)
    elif load_col and load_col in df.columns:
        assert cross_section_area is not None and cross_section_area > 0, (
            "cross_section_area is required for load-to-stress conversion"
        )
        load = df[load_col].to_numpy(dtype=np.float64)
        stress = load / cross_section_area
    else:
        assert False, "No stress or load column available"

    # NaN行を除外
    valid_mask = ~(np.isnan(strain) | np.isnan(stress))
    strain = strain[valid_mask]
    stress = stress[valid_mask]

    return strain, stress


def _detect_encoding(content: bytes) -> str:
    """エンコーディングを推定する."""
    # BOMチェック
    if content.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"

    # UTF-8でデコードを試行
    try:
        content.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        pass

    # Shift_JISを試行（日本語CSVで一般的）
    try:
        content.decode("shift_jis")
        return "shift_jis"
    except UnicodeDecodeError:
        pass

    return "latin-1"


def _detect_delimiter(text: str) -> str:
    """区切り文字を推定する."""
    first_lines = text.split("\n")[:5]
    sample = "\n".join(first_lines)

    # タブ区切りの検出
    tab_count = sample.count("\t")
    comma_count = sample.count(",")
    semicolon_count = sample.count(";")

    counts = {"\t": tab_count, ",": comma_count, ";": semicolon_count}
    return max(counts, key=counts.get)


def _find_matching_column(
    columns: list[str],
    patterns: list[re.Pattern],
) -> str | None:
    """パターンに一致する列名を検索する."""
    for pattern in patterns:
        for col in columns:
            if pattern.search(col):
                return col
    return None
