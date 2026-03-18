"use client";

import { useSpecimenStore } from "@/stores/specimenStore";
import { FileUploader } from "@/components/upload/FileUploader";

export function LeftPanel() {
  const { datasets, selectedDatasetId, selectDataset, analyses, selectedAnalysisId, selectAnalysis } =
    useSpecimenStore();

  return (
    <div className="flex flex-col border-r border-border bg-panel-bg overflow-y-auto">
      {/* Upload section */}
      <div className="border-b border-border p-3">
        <h2 className="mb-2 text-sm font-semibold text-foreground/70 uppercase tracking-wide">
          Upload
        </h2>
        <FileUploader />
      </div>

      {/* Dataset list */}
      <div className="border-b border-border p-3">
        <h2 className="mb-2 text-sm font-semibold text-foreground/70 uppercase tracking-wide">
          Datasets
        </h2>
        {datasets.length === 0 ? (
          <p className="text-sm text-foreground/50">No datasets uploaded</p>
        ) : (
          <ul className="space-y-1">
            {datasets.map((ds) => (
              <li key={ds.dataset_id}>
                <button
                  onClick={() => selectDataset(ds.dataset_id)}
                  className={`w-full rounded px-2 py-1.5 text-left text-sm transition-colors ${
                    selectedDatasetId === ds.dataset_id
                      ? "bg-primary/10 text-primary font-medium"
                      : "hover:bg-foreground/5"
                  }`}
                >
                  <span className="block truncate">{ds.filename}</span>
                  <span className="text-xs text-foreground/50">
                    {ds.row_count} rows, {ds.detected_columns.length} cols
                  </span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Analysis list */}
      <div className="p-3">
        <h2 className="mb-2 text-sm font-semibold text-foreground/70 uppercase tracking-wide">
          Analyses
        </h2>
        {analyses.length === 0 ? (
          <p className="text-sm text-foreground/50">No analyses yet</p>
        ) : (
          <ul className="space-y-1">
            {analyses.map((a) => (
              <li key={a.analysis_id}>
                <button
                  onClick={() => selectAnalysis(a.analysis_id)}
                  className={`w-full rounded px-2 py-1.5 text-left text-sm transition-colors ${
                    selectedAnalysisId === a.analysis_id
                      ? "bg-primary/10 text-primary font-medium"
                      : "hover:bg-foreground/5"
                  }`}
                >
                  <span className="block truncate">{a.specimen_name}</span>
                  <span className="text-xs text-foreground/50">
                    E={a.results.youngs_modulus_gpa.toFixed(1)} GPa
                  </span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
