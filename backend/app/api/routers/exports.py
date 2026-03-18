"""エクスポートAPIルーター."""

import csv
import io

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.services.analysis_service import get_analysis, get_analysis_store

router = APIRouter(tags=["exports"])


@router.get("/analyses/{analysis_id}/export/csv")
async def export_csv(analysis_id: str) -> StreamingResponse:
    """解析結果をCSVとしてエクスポートする.

    計算条件も含めて出力する。

    Args:
        analysis_id: 解析ID

    Returns:
        CSVファイルのストリーミングレスポンス
    """
    try:
        response = get_analysis(analysis_id)
    except AssertionError:
        raise HTTPException(status_code=404, detail="Analysis not found")

    output = io.StringIO()
    writer = csv.writer(output)

    # ヘッダー: メタ情報
    writer.writerow(["# Stress-Strain Analysis Results"])
    writer.writerow(["# Specimen", response.specimen_name])
    writer.writerow(
        ["# Young's Modulus Method", response.calculation_context.youngs_modulus_method]
    )
    writer.writerow(
        ["# Young's Modulus R²", f"{response.calculation_context.youngs_modulus_r_squared:.6f}"]
    )
    writer.writerow([])

    # 結果テーブル
    writer.writerow(["Property", "Value", "Unit"])
    r = response.results
    writer.writerow(["Young's Modulus", f"{r.youngs_modulus_gpa:.2f}", "GPa"])
    ys_str = f"{r.yield_strength_02_mpa:.1f}" if r.yield_strength_02_mpa is not None else "N/A"
    writer.writerow(["0.2% Yield Strength", ys_str, "MPa"])
    writer.writerow(["UTS", f"{r.ultimate_tensile_strength_mpa:.1f}", "MPa"])
    writer.writerow(
        ["Uniform Elongation", f"{r.uniform_elongation_percent:.2f}", "%"]
    )
    writer.writerow(
        ["Fracture Strain", f"{r.fracture_strain_percent:.2f}", "%"]
    )
    writer.writerow(["Toughness", f"{r.toughness_mj_m3:.2f}", "MJ/m³"])

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{response.specimen_name}_results.csv"'
            )
        },
    )
