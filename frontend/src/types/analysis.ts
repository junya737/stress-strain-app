import type { ColumnMapping } from "./specimen";

/** 解析リクエスト */
export interface AnalysisRequest {
  dataset_id: string;
  specimen_name: string;
  column_mapping: ColumnMapping;
  youngs_modulus_strain_range: [number, number] | null;
  yield_offset: number;
  trim_range: [number, number] | null;
}

/** 機械的特性レスポンス */
export interface MechanicalPropertiesResponse {
  youngs_modulus_gpa: number;
  yield_strength_02_mpa: number | null;
  ultimate_tensile_strength_mpa: number;
  uniform_elongation_percent: number;
  fracture_strain_percent: number;
  toughness_mj_m3: number;
}

/** 計算条件レスポンス */
export interface CalculationContextResponse {
  youngs_modulus_fit_range: [number, number];
  youngs_modulus_r_squared: number;
  youngs_modulus_data_points: number;
  youngs_modulus_method: string;
  yield_offset_used: number;
  yield_intersection_found: boolean;
  trim_range_applied: [number, number] | null;
  input_units: Record<string, string>;
  conversion_applied: string[];
}

/** 注釈点 */
export interface AnnotationPoint {
  label: string;
  strain: number;
  stress: number;
}

/** 曲線データレスポンス */
export interface CurveDataResponse {
  strain: number[];
  stress: number[];
  curve_type: string;
  regression_line: { strain: number[]; stress: number[] } | null;
  offset_line: { strain: number[]; stress: number[] } | null;
  annotation_points: AnnotationPoint[];
}

/** 警告レスポンス */
export interface WarningResponse {
  metric: string;
  message: string;
  severity: string;
}

/** 解析結果レスポンス */
export interface AnalysisResponse {
  analysis_id: string;
  specimen_name: string;
  results: MechanicalPropertiesResponse;
  calculation_context: CalculationContextResponse;
  curve_data: CurveDataResponse;
  warnings: WarningResponse[];
}
