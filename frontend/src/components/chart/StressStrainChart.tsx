"use client";

import dynamic from "next/dynamic";
import type { AnalysisResponse } from "@/types/analysis";

// Plotlyはクライアントサイドのみで動作するためdynamic importが必要
const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

interface Props {
  analysis: AnalysisResponse;
}

export function StressStrainChart({ analysis }: Props) {
  const { curve_data, results } = analysis;

  const traces: Plotly.Data[] = [
    // Main curve
    {
      x: curve_data.strain,
      y: curve_data.stress,
      type: "scattergl",
      mode: "lines",
      name: analysis.specimen_name,
      line: { color: "#2563eb", width: 2 },
      hovertemplate:
        "ε = %{x:.4f}<br>σ = %{y:.1f} MPa<extra></extra>",
    },
  ];

  // Regression line (Young's modulus)
  if (curve_data.regression_line) {
    traces.push({
      x: curve_data.regression_line.strain,
      y: curve_data.regression_line.stress,
      type: "scatter",
      mode: "lines",
      name: `E = ${results.youngs_modulus_gpa.toFixed(1)} GPa`,
      line: { color: "#16a34a", width: 1.5, dash: "dash" },
      hoverinfo: "skip",
    });
  }

  // Offset line (0.2% yield)
  if (curve_data.offset_line) {
    traces.push({
      x: curve_data.offset_line.strain,
      y: curve_data.offset_line.stress,
      type: "scatter",
      mode: "lines",
      name: "0.2% Offset",
      line: { color: "#d97706", width: 1, dash: "dot" },
      hoverinfo: "skip",
    });
  }

  // Annotation points (UTS, yield, fracture)
  const markerColors: Record<string, string> = {
    UTS: "#dc2626",
    "0.2% Yield": "#d97706",
    Fracture: "#6b7280",
  };

  if (curve_data.annotation_points.length > 0) {
    traces.push({
      x: curve_data.annotation_points.map((p) => p.strain),
      y: curve_data.annotation_points.map((p) => p.stress),
      type: "scatter",
      mode: "markers+text" as Plotly.PlotData["mode"],
      name: "Key Points",
      marker: {
        size: 10,
        color: curve_data.annotation_points.map(
          (p) => markerColors[p.label] ?? "#2563eb"
        ),
        symbol: "diamond",
      },
      text: curve_data.annotation_points.map((p) => p.label),
      textposition: "top center",
      textfont: { size: 11 },
      hovertemplate:
        "%{text}<br>ε = %{x:.4f}<br>σ = %{y:.1f} MPa<extra></extra>",
    });
  }

  const layout: Partial<Plotly.Layout> = {
    xaxis: {
      title: { text: "Strain", font: { size: 14 } },
      zeroline: true,
      gridcolor: "#e2e8f0",
    },
    yaxis: {
      title: { text: "Stress (MPa)", font: { size: 14 } },
      zeroline: true,
      gridcolor: "#e2e8f0",
    },
    legend: {
      x: 0.02,
      y: 0.98,
      bgcolor: "rgba(255,255,255,0.8)",
      bordercolor: "#e2e8f0",
      borderwidth: 1,
    },
    margin: { l: 60, r: 20, t: 30, b: 50 },
    hovermode: "closest",
    plot_bgcolor: "#ffffff",
    paper_bgcolor: "#ffffff",
  };

  const config: Partial<Plotly.Config> = {
    responsive: true,
    displayModeBar: true,
    modeBarButtonsToRemove: ["lasso2d", "select2d"],
    toImageButtonOptions: {
      format: "png",
      width: 1200,
      height: 800,
      scale: 2,
    },
  };

  return (
    <div className="h-full w-full">
      <Plot
        data={traces}
        layout={layout}
        config={config}
        useResizeHandler
        className="h-full w-full"
        style={{ width: "100%", height: "100%" }}
      />
    </div>
  );
}
