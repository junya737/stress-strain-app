"use client";

import { useSpecimenStore } from "@/stores/specimenStore";
import { ResultsTable } from "@/components/analysis/ResultsTable";
import { CalculationContext } from "@/components/analysis/CalculationContext";
import { ExportPanel } from "@/components/export/ExportPanel";

export function RightPanel() {
  const { selectedAnalysisId, analyses } = useSpecimenStore();

  const selectedAnalysis = analyses.find(
    (a) => a.analysis_id === selectedAnalysisId
  );

  return (
    <div className="flex flex-col border-l border-border bg-panel-bg overflow-y-auto">
      {selectedAnalysis ? (
        <>
          {/* Results */}
          <div className="border-b border-border p-3">
            <h2 className="mb-2 text-sm font-semibold text-foreground/70 uppercase tracking-wide">
              Results
            </h2>
            <ResultsTable results={selectedAnalysis.results} />
          </div>

          {/* Calculation Context */}
          <div className="border-b border-border p-3">
            <h2 className="mb-2 text-sm font-semibold text-foreground/70 uppercase tracking-wide">
              Calculation Details
            </h2>
            <CalculationContext context={selectedAnalysis.calculation_context} />
          </div>

          {/* Warnings */}
          {selectedAnalysis.warnings.length > 0 && (
            <div className="border-b border-border p-3">
              <h2 className="mb-2 text-sm font-semibold text-warning uppercase tracking-wide">
                Warnings
              </h2>
              <ul className="space-y-1">
                {selectedAnalysis.warnings.map((w, i) => (
                  <li
                    key={i}
                    className="rounded bg-warning/10 px-2 py-1 text-xs text-warning"
                  >
                    [{w.metric}] {w.message}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Export */}
          <div className="p-3">
            <h2 className="mb-2 text-sm font-semibold text-foreground/70 uppercase tracking-wide">
              Export
            </h2>
            <ExportPanel analysisId={selectedAnalysis.analysis_id} />
          </div>
        </>
      ) : (
        <div className="flex h-full items-center justify-center p-4">
          <p className="text-center text-sm text-foreground/40">
            Run an analysis to see results
          </p>
        </div>
      )}
    </div>
  );
}
