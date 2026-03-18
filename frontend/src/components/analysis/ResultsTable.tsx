"use client";

import type { MechanicalPropertiesResponse } from "@/types/analysis";

interface Props {
  results: MechanicalPropertiesResponse;
}

interface ResultRow {
  label: string;
  value: string;
  unit: string;
}

export function ResultsTable({ results }: Props) {
  const rows: ResultRow[] = [
    {
      label: "Young's Modulus",
      value: results.youngs_modulus_gpa.toFixed(1),
      unit: "GPa",
    },
    {
      label: "0.2% Yield Strength",
      value:
        results.yield_strength_02_mpa != null
          ? results.yield_strength_02_mpa.toFixed(1)
          : "N/A",
      unit: "MPa",
    },
    {
      label: "UTS",
      value: results.ultimate_tensile_strength_mpa.toFixed(1),
      unit: "MPa",
    },
    {
      label: "Uniform Elongation",
      value: results.uniform_elongation_percent.toFixed(2),
      unit: "%",
    },
    {
      label: "Fracture Strain",
      value: results.fracture_strain_percent.toFixed(2),
      unit: "%",
    },
    {
      label: "Toughness",
      value: results.toughness_mj_m3.toFixed(2),
      unit: "MJ/m³",
    },
  ];

  return (
    <table className="w-full text-sm">
      <tbody>
        {rows.map((row) => (
          <tr key={row.label} className="border-b border-border last:border-0">
            <td className="py-1.5 text-foreground/70">{row.label}</td>
            <td className="py-1.5 text-right font-mono font-medium">
              {row.value}
            </td>
            <td className="py-1.5 pl-1 text-xs text-foreground/50">
              {row.unit}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
