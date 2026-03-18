
# Kaggle Operations & Workflow

このドキュメントは、Kaggle関連のリソース（Notebook, Data, Discussion）の操作と管理場所に関するルールを定義します。

**【重要】既存の処理フローやディレクトリ構造を厳守してください。勝手な構成変更は禁止です。**

## ℹ️ Competition Knowledge
コンペティションの前提知識（ゴール、評価指標、データの定義など）は以下のファイルで管理されています。
分析や実装を行う前に、必ずこれらのファイルを参照してください。

- **Competition Overview**: `.claude/rules/kaggle/competition-info/overview.md`
  - コンペの目的、タスクの種類、評価指標（Metric）の詳細。
- **Dataset Description**: `.claude/rules/kaggle/competition-info/dataset.md`
  - 各ファイルのカラム定義、データの構造、重要な特徴量の意味。

## 📥 Resource Management (Download & Save)

Kaggle APIを使用してリソースを取得する際は、以下のパス定義に従ってください。

### 1. Kaggle Notebooks (Kernels)

#### 2025 Current Competition (Main)
- **保存場所**: `reference/notebooks/`
- **まとめ保存場所**: `reference/notebooks_md/`
- **要約ルール**: `/summarize-notebook` スキルを使用
- **コマンド例**:
```bash
  # ディレクトリ移動してから実行
  cd reference/notebooks/
  kaggle kernels pull {username}/{notebook-name}
  # 例: kaggle kernels pull sohier/cmi-2025-demo-submission
```

#### Reference Competitions (Past/External)
他コンペや過去のコンペを参照する場合のルールです。

- **保存場所**: `reference/{competition_name}/notebooks/`
  - コンペごとにディレクトリを作成して整理してください。
- **まとめ保存場所**: `reference/{competition_name}/notebooks_md/`
- **目的**: 過去の解法、ベースライン、類似タスクの技術参照用
- **コマンド例**:
```bash
  # ディレクトリがない場合は作成
  mkdir -p reference/{competition_name}/notebooks
  cd reference/{competition_name}/notebooks
  
  # ダウンロード実行
  kaggle kernels pull {username}/{notebook-name}
```
**⚠️ 注意**: ノートブックをまとめた後は、その内容をチャットログに出力しないでください。「保存完了」のみ報告してください。


### 2. Kaggle Datasets

* **コマンド**:
```bash
kaggle competitions download -c cmi-detect-behavior-with-sensor-data
```


* **補足**: APIは認証済みです。ダウンロード後は `data/raw/` 等の適切な場所に配置してください。

### 3. Discussions

* **保存場所**: `reference/discussions/`
* **要約ルール**: `/summarize-discussion` スキルを使用

### 4. Solutions (Past Competitions)

* **保存場所**: `reference/{competition_name}/solutions/`
* **説明**: 過去のコンペ等の解法。
* **要約ルール**: `/summarize-discussion` スキルを使用

---

## 🧠 Strategy Planning

* **保存場所**: `reference/strategy/`
* **要約ルール**: `/summarize-strategy` スキルを使用
* **運用**:
* 「次の戦略をまとめて」と指示された場合は、このディレクトリにMDファイルとして保存してください。

