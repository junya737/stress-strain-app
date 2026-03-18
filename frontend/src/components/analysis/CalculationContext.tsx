"use client";

import type { CalculationContextResponse } from "@/types/analysis";

interface Props {
  context: CalculationContextResponse;
}

export function CalculationContext({ context }: Props) {
  return (
    <div className="space-y-2 text-xs">
      {/* Young's Modulus details */}
      <div>
        <span className="font-medium text-foreground/70">
          E fit range:
        </span>{" "}
        <span className="font-mono">
          [{context.youngs_modulus_fit_range[0].toFixed(5)},{" "}
          {context.youngs_modulus_fit_range[1].toFixed(5)}]
        </span>
      </div>
      <div>
        <span className="font-medium text-foreground/70">R²:</span>{" "}
        <span
          className={`font-mono font-medium ${
            context.youngs_modulus_r_squared >= 0.999
              ? "text-success"
              : context.youngs_modulus_r_squared >= 0.99
                ? "text-warning"
                : "text-error"
          }`}
        >
          {context.youngs_modulus_r_squared.toFixed(6)}
        </span>
      </div>
      <div>
        <span className="font-medium text-foreground/70">Data points:</span>{" "}
        <span className="font-mono">{context.youngs_modulus_data_points}</span>
      </div>
      <div>
        <span className="font-medium text-foreground/70">Method:</span>{" "}
        <span
          className={`rounded px-1 py-0.5 text-[10px] font-medium uppercase ${
            context.youngs_modulus_method === "auto"
              ? "bg-primary/10 text-primary"
              : "bg-warning/10 text-warning"
          }`}
        >
          {context.youngs_modulus_method}
        </span>
      </div>
      <div>
        <span className="font-medium text-foreground/70">Yield offset:</span>{" "}
        <span className="font-mono">
          {(context.yield_offset_used * 100).toFixed(1)}%
        </span>
      </div>
      <div>
        <span className="font-medium text-foreground/70">
          Yield intersection:
        </span>{" "}
        <span
          className={
            context.yield_intersection_found ? "text-success" : "text-error"
          }
        >
          {context.yield_intersection_found ? "Found" : "Not found"}
        </span>
      </div>

      {/* Conversion info */}
      {context.conversion_applied.length > 0 && (
        <div>
          <span className="font-medium text-foreground/70">Conversions:</span>
          <ul className="mt-0.5 list-inside list-disc text-foreground/60">
            {context.conversion_applied.map((c, i) => (
              <li key={i}>{c}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
