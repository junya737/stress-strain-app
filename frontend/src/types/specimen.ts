/** 列マッピング + 試験片パラメータ */
export interface ColumnMapping {
  strain_column: string;
  stress_column: string | null;
  load_column: string | null;
  displacement_column: string | null;
  cross_section_area: number | null;
  gauge_length: number | null;
  strain_unit: "dimensionless" | "percent" | "microstrain";
  stress_unit: "MPa" | "GPa" | "ksi";
}

/** CSVアップロードレスポンス */
export interface DatasetResponse {
  dataset_id: string;
  filename: string;
  detected_columns: string[];
  row_count: number;
  preview: Record<string, unknown>[];
  suggested_mapping: ColumnMapping | null;
  detected_encoding: string;
  detected_delimiter: string;
}
