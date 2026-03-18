"use client";

import { useState } from "react";
import { useSpecimenStore } from "@/stores/specimenStore";
import { runAnalysis } from "@/lib/apiClient";
import type { DatasetResponse, ColumnMapping } from "@/types/specimen";

interface Props {
  dataset: DatasetResponse;
  initialMapping: ColumnMapping | null;
}

export function ColumnMapper({ dataset, initialMapping }: Props) {
  const { addAnalysis, setLoading, setError } = useSpecimenStore();

  const [specimenName, setSpecimenName] = useState(
    dataset.filename.replace(/\.\w+$/, "")
  );
  const [strainCol, setStrainCol] = useState(
    initialMapping?.strain_column ?? ""
  );
  const [stressCol, setStressCol] = useState(
    initialMapping?.stress_column ?? ""
  );
  const [loadCol, setLoadCol] = useState(initialMapping?.load_column ?? "");
  const [dispCol, setDispCol] = useState(
    initialMapping?.displacement_column ?? ""
  );
  const [crossSection, setCrossSection] = useState("");
  const [gaugeLength, setGaugeLength] = useState("");
  const [strainUnit, setStrainUnit] = useState<ColumnMapping["strain_unit"]>(
    initialMapping?.strain_unit ?? "dimensionless"
  );
  const [stressUnit, setStressUnit] = useState<ColumnMapping["stress_unit"]>(
    initialMapping?.stress_unit ?? "MPa"
  );

  const cols = dataset.detected_columns;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const mapping: ColumnMapping = {
        strain_column: strainCol,
        stress_column: stressCol || null,
        load_column: loadCol || null,
        displacement_column: dispCol || null,
        cross_section_area: crossSection ? parseFloat(crossSection) : null,
        gauge_length: gaugeLength ? parseFloat(gaugeLength) : null,
        strain_unit: strainUnit,
        stress_unit: stressUnit,
      };

      const result = await runAnalysis({
        dataset_id: dataset.dataset_id,
        specimen_name: specimenName,
        column_mapping: mapping,
        youngs_modulus_strain_range: null,
        yield_offset: 0.002,
        trim_range: null,
      });

      addAnalysis(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const selectClass =
    "w-full rounded border border-border bg-background px-2 py-1.5 text-sm focus:border-primary focus:outline-none";
  const inputClass = selectClass;
  const labelClass = "block text-xs font-medium text-foreground/70 mb-1";

  return (
    <div className="mx-auto max-w-lg p-8">
      <h2 className="mb-4 text-xl font-semibold">Column Mapping</h2>
      <p className="mb-6 text-sm text-foreground/60">
        Map CSV columns to stress-strain data fields for{" "}
        <span className="font-medium">{dataset.filename}</span> ({dataset.row_count}{" "}
        rows)
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Specimen Name */}
        <div>
          <label className={labelClass}>Specimen Name</label>
          <input
            type="text"
            value={specimenName}
            onChange={(e) => setSpecimenName(e.target.value)}
            className={inputClass}
            required
          />
        </div>

        {/* Strain Column */}
        <div>
          <label className={labelClass}>Strain Column *</label>
          <select
            value={strainCol}
            onChange={(e) => setStrainCol(e.target.value)}
            className={selectClass}
            required
          >
            <option value="">-- Select --</option>
            {cols.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>

        {/* Strain Unit */}
        <div>
          <label className={labelClass}>Strain Unit</label>
          <select
            value={strainUnit}
            onChange={(e) =>
              setStrainUnit(e.target.value as ColumnMapping["strain_unit"])
            }
            className={selectClass}
          >
            <option value="dimensionless">Dimensionless (0.001)</option>
            <option value="percent">Percent (0.1%)</option>
            <option value="microstrain">Microstrain (1000 με)</option>
          </select>
        </div>

        {/* Stress Column */}
        <div>
          <label className={labelClass}>Stress Column</label>
          <select
            value={stressCol}
            onChange={(e) => setStressCol(e.target.value)}
            className={selectClass}
          >
            <option value="">-- None --</option>
            {cols.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>

        {/* Stress Unit */}
        <div>
          <label className={labelClass}>Stress Unit</label>
          <select
            value={stressUnit}
            onChange={(e) =>
              setStressUnit(e.target.value as ColumnMapping["stress_unit"])
            }
            className={selectClass}
          >
            <option value="MPa">MPa</option>
            <option value="GPa">GPa</option>
            <option value="ksi">ksi</option>
          </select>
        </div>

        {/* Load / Displacement (optional) */}
        <details className="rounded border border-border p-3">
          <summary className="cursor-pointer text-sm font-medium text-foreground/70">
            Load / Displacement (optional)
          </summary>
          <div className="mt-3 space-y-3">
            <div>
              <label className={labelClass}>Load Column</label>
              <select
                value={loadCol}
                onChange={(e) => setLoadCol(e.target.value)}
                className={selectClass}
              >
                <option value="">-- None --</option>
                {cols.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className={labelClass}>Displacement Column</label>
              <select
                value={dispCol}
                onChange={(e) => setDispCol(e.target.value)}
                className={selectClass}
              >
                <option value="">-- None --</option>
                {cols.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className={labelClass}>Cross-Section Area (mm²)</label>
              <input
                type="number"
                step="any"
                value={crossSection}
                onChange={(e) => setCrossSection(e.target.value)}
                className={inputClass}
                placeholder="e.g. 12.57"
              />
            </div>
            <div>
              <label className={labelClass}>Gauge Length (mm)</label>
              <input
                type="number"
                step="any"
                value={gaugeLength}
                onChange={(e) => setGaugeLength(e.target.value)}
                className={inputClass}
                placeholder="e.g. 50"
              />
            </div>
          </div>
        </details>

        <button
          type="submit"
          className="w-full rounded bg-primary px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-hover"
        >
          Run Analysis
        </button>
      </form>

      {/* Data Preview */}
      {dataset.preview.length > 0 && (
        <div className="mt-6">
          <h3 className="mb-2 text-sm font-semibold text-foreground/70">
            Data Preview
          </h3>
          <div className="overflow-x-auto rounded border border-border">
            <table className="w-full text-xs">
              <thead>
                <tr className="bg-foreground/5">
                  {cols.map((c) => (
                    <th key={c} className="px-2 py-1 text-left font-medium">
                      {c}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {dataset.preview.map((row, i) => (
                  <tr key={i} className="border-t border-border">
                    {cols.map((c) => (
                      <td key={c} className="px-2 py-1 font-mono">
                        {String(row[c] ?? "")}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
