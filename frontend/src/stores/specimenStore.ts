import { create } from "zustand";
import type { DatasetResponse, ColumnMapping } from "@/types/specimen";
import type { AnalysisResponse } from "@/types/analysis";

interface SpecimenState {
  /** アップロード済みデータセット */
  datasets: DatasetResponse[];
  /** 選択中のデータセットID */
  selectedDatasetId: string | null;
  /** 列マッピング */
  columnMapping: ColumnMapping | null;
  /** 解析結果一覧 */
  analyses: AnalysisResponse[];
  /** 選択中の解析ID */
  selectedAnalysisId: string | null;
  /** ローディング状態 */
  isLoading: boolean;
  /** エラーメッセージ */
  error: string | null;

  /** データセット追加 */
  addDataset: (ds: DatasetResponse) => void;
  /** データセット選択 */
  selectDataset: (id: string) => void;
  /** 列マッピング設定 */
  setColumnMapping: (mapping: ColumnMapping) => void;
  /** 解析結果追加 */
  addAnalysis: (analysis: AnalysisResponse) => void;
  /** 解析結果選択 */
  selectAnalysis: (id: string) => void;
  /** ローディング状態設定 */
  setLoading: (loading: boolean) => void;
  /** エラー設定 */
  setError: (error: string | null) => void;
}

export const useSpecimenStore = create<SpecimenState>((set) => ({
  datasets: [],
  selectedDatasetId: null,
  columnMapping: null,
  analyses: [],
  selectedAnalysisId: null,
  isLoading: false,
  error: null,

  addDataset: (ds) =>
    set((state) => ({
      datasets: [...state.datasets, ds],
      selectedDatasetId: ds.dataset_id,
      columnMapping: ds.suggested_mapping,
    })),

  selectDataset: (id) => set({ selectedDatasetId: id }),

  setColumnMapping: (mapping) => set({ columnMapping: mapping }),

  addAnalysis: (analysis) =>
    set((state) => ({
      analyses: [...state.analyses, analysis],
      selectedAnalysisId: analysis.analysis_id,
    })),

  selectAnalysis: (id) => set({ selectedAnalysisId: id }),

  setLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error }),
}));
