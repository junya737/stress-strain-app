"use client";

import { getExportCsvUrl } from "@/lib/apiClient";

interface Props {
  analysisId: string;
}

export function ExportPanel({ analysisId }: Props) {
  const handleExportCsv = () => {
    const url = getExportCsvUrl(analysisId);
    window.open(url, "_blank");
  };

  return (
    <div className="space-y-2">
      <button
        onClick={handleExportCsv}
        className="w-full rounded border border-border px-3 py-1.5 text-sm transition-colors hover:bg-foreground/5"
      >
        Export Results (CSV)
      </button>
      <p className="text-[10px] text-foreground/40">
        Image export: Use the camera icon in the chart toolbar
      </p>
    </div>
  );
}
