"use client";

import { useSpecimenStore } from "@/stores/specimenStore";
import { StressStrainChart } from "@/components/chart/StressStrainChart";
import { ColumnMapper } from "@/components/upload/ColumnMapper";

export function CenterPanel() {
  const { selectedDatasetId, selectedAnalysisId, analyses, datasets, columnMapping } =
    useSpecimenStore();

  const selectedAnalysis = analyses.find(
    (a) => a.analysis_id === selectedAnalysisId
  );

  const selectedDataset = datasets.find(
    (d) => d.dataset_id === selectedDatasetId
  );

  // Show column mapper if dataset is selected but no analysis yet
  const needsMapping = selectedDataset && !selectedAnalysis && selectedDatasetId;

  return (
    <div className="flex flex-col overflow-hidden bg-background">
      {/* Chart area */}
      <div className="flex-1 p-4">
        {selectedAnalysis ? (
          <StressStrainChart analysis={selectedAnalysis} />
        ) : needsMapping ? (
          <ColumnMapper
            dataset={selectedDataset}
            initialMapping={columnMapping}
          />
        ) : (
          <div className="flex h-full items-center justify-center">
            <div className="text-center text-foreground/40">
              <svg
                className="mx-auto mb-4 h-16 w-16"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1}
                  d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <p className="text-lg font-medium">Upload a CSV to get started</p>
              <p className="mt-1 text-sm">
                Drag & drop or click to upload stress-strain data
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
