# Python Coding Guidelines

このドキュメントは、Pythonコードの実装、修正、リファクタリングに関する厳格なルールを定義します。

## 🏗 Architecture & Design

### ⚖️ Balance: Simplicity vs. Robustness
すべてのコードにデザインパターンを適用する必要はありません。タスクの性質に応じて、以下の基準で実装方針を使い分けてください。

1.  **Simple Implementation**:
    - **対象**: 使い捨ての分析スクリプト、プロトタイプ、小規模な修正。
    - **方針**: YAGNI (You Aren't Gonna Need It) を重視。過度な抽象化を避ける。
2.  **Robust Implementation**:
    - **対象**: 再利用可能なモジュール (`module/`), メインの学習パイプライン, 長期間メンテナンスするコード。
    - **方針**: SOLID原則、デザインパターンを適用し、拡張性を確保する。

**【重要】実装方針の確認 (Ask User)**
新規機能の実装や大規模なリファクタリングを行う際は、作業着手前に以下の選択肢をユーザーに提示し、方針を確認すること：
> 「この機能は、将来的な拡張を見越して『デザインパターンを用いた堅牢な設計』にしますか？ それとも可読性を優先した『シンプルな実装』にしますか？」

---

### 推奨するデザインパターンと設計原則
（※ユーザーが「堅牢な設計」を選択した場合、または既存コードが既にパターン化されている場合は以下に従うこと）

1.  **Inheritance vs. Composition**
    - **Inheritance の使用基準**:
      - **「インターフェースの定義」**には継承を積極的に使用する。
      - 具体的には、`abc.ABC` を継承した抽象基底クラスを作成し、具体的な処理はサブクラスで実装する形式（Template Method パターンや Strategy パターンの基盤）は推奨される。
      - **禁止事項**: 実装の再利用のみを目的とした深い継承階層（3階層以上など）は避けること。
    - **Composition の使用基準**:
      - 既存のクラスに機能を追加・拡張したい場合は、継承ではなく、そのクラスをフィールドとして持つ「コンポジション」を使用すること。

2.  **Strategy Pattern**
    - アルゴリズム（前処理、Loss等）を切り替える際は、`if-else` 分岐ではなく、**共通の抽象基底クラス**を継承した具象クラスとして実装することを検討する。

3.  **Dependency Injection**
    - テスト容易性向上のため、依存オブジェクトは内部で生成せず `__init__` で受け取る設計を推奨する。

4.  **Factory Pattern**
    - 条件分岐による生成ロジックが散乱する場合は、Factoryの使用を検討する。

### 実装の基本方針
- **既存パターンの踏襲**: 修正時は、既存のコードがシンプルならシンプルに、構造化されているなら構造化して実装すること（一貫性の維持）。
- **オブジェクト指向**: 責任範囲を明確にするため、適切な粒度でクラスを使用すること。
- **I/O操作はmain関数で実行**: ファイルの読み込み・書き込みはmain関数内で明示的に行い、処理関数にはデータを引数として渡すこと。I/Oを関数内で隠蔽すると不透明性が増す。

### データ構造
- **Dataclass**: 設定値やデータの束（Config, Result等）の管理には、`dict` ではなく `dataclass` (frozen=True推奨) を使用すること。
  - 理由: 型ヒントが効き、IDEや静的解析の恩恵を受けるため。

### 型安全性
- **型アノテーション必須**:
  - 関数の引数と戻り値の型を明示すること。
  - クラスのフィールド（メンバ変数）の型を明示すること。
  - 関数内でも、誤解を招きそうな変数には型ヒントを付与すること。
- **Assertion**: 前提条件の確認には `assert` を使用し、契約プログラミングを意識すること。

### エラーハンドリング
- **Fail Fast**: 想定外の値が来た場合はフォールバック（デフォルト値での救済）をせず、直ちに `AssertionError` 等で停止させること。
- **Try-Except 禁止**: エラーを隠蔽するリスクがあるため `try-except` ブロックは使用しないこと。

### 📦 Module Structure
- **モジュールパッケージ**: 再利用可能なコード（Config定義、データ処理、評価ロジック等）はプロジェクト専用パッケージ配下に配置すること。パッケージ名はプロジェクトの内容がわかる名前にする（例: `deep_past/`, `biomass/`）。
- **Config定義**: パッケージ内の `configs/` に配置する。モデル設定（学習・推論で共有）、学習設定、推論設定を分離して定義すること。
- **スクリプト**: `scripts/` に配置し、パッケージからの絶対インポートを使用する。

### ⚙️ Configuration Management
- **パス型は `str`**: dataclass内でパスを定義する際は `Path` ではなく `str` を使用すること。関数内で必要に応じて `Path()` に変換する。
- **Debugモード実装**: データセット準備・学習・推論スクリプトには `--debug` / `-d` フラグを実装すること。debugモード時のサンプル数は `debug_samples` としてConfigに定義し、データを制限して高速に動作確認できるようにする。
- **成果物の保存パス**: データセット生成・訓練・推論の成果物は `base_dir/<JST時刻>/` 配下に保存すること。debugモード時は `base_dir/debug/<JST時刻>/` に保存する。JST時刻の形式は `YYYYMMDD_HHMM`（例: `20260114_1915`）とし、config の `__post_init__` で定義する。
- **Configの保存**: 実験の再現性のため、config は成果物と同じディレクトリに `config.json` として保存すること。
- **Config設計（コンポジション）**:
  - **モデルConfig**: モデル固有の設定（model_name, max_length, epochs, lr, batch_size, num_beams等）を1つの `dataclass` にまとめる。モデルを切り替えるだけで適切なハイパーパラメータが付いてくる設計にすること。
  - **タスクConfig**: 学習・推論などタスクごとのConfigは、モデルConfigを**フィールドとして持つ（コンポジション）**。タスクConfig自体にはモデルに依存しない設定（パス、seed、debug等）のみ定義する。継承は使用しない。
  - **モデル追加時**: モデルConfigクラスを新規追加し、タスクConfigの `model` フィールドのデフォルトを差し替えるだけで切り替え可能にする。

---

## 📝 Language & Logging Rules

情報の種類によって言語を使い分けてください。

| 項目 | 言語 | 備考 |
| :--- | :--- | :--- |
| **Docstring** | 日本語 | 詳細な説明記述用 |
| **コメント** | 日本語 | 実装意図の補足用 |
| **ログ (Logs)** | **英語** | システムログ、エラーメッセージ |
| **Debug Print** | **英語** | デバッグ出力 |
| **Plot (図表)** | **英語** | タイトル、軸ラベル、凡例 |

---

## 🚀 Execution Standards 

Pythonスクリプトを実行する際の環境とカレントディレクトリに関する厳格なルールです。

### 1. Project Root Principle
- **ルール**: すべてのスクリプトは、**プロジェクトのルートディレクトリ**をカレントディレクトリとして実行されることを前提に実装・実行すること。
- **コマンド例**:
  - ✅ `python scripts/analysis_task.py`
  - ❌ `cd scripts && python analysis_task.py`
- **sys.pathの扱い**:
  - `scripts/` 内のファイルなどで、親ディレクトリを `sys.path` に追加するコード（`sys.path.append(...)` 等）が含まれている場合、それはルート実行環境でモジュール解決を行うための必須コードです。**安易に削除・変更しないでください**。

### 2. Environment Compatibility
コードやディレクトリ構造を修正する際は、以下の両方の環境で動作することを保証してください：
1. **ローカル環境**: `python scripts/xxx.py` で正常に動作すること。
2. **ターゲット環境**: 本番サーバー、CI/CD、コンペティション環境（Kaggle Kernel等）でもパスが解決できること。

---

## 📦 Import Conventions

上記の実行基準（ルート実行）に基づき、以下のインポートスタイルを厳守してください。

### 1. Absolute Imports Only
- **ルール**: プロジェクト内の自作モジュール（`module/` や `src/` 等）をインポートする際は、必ずルートからのパスを指定する**絶対インポート**を使用すること。
- **禁止**: 相対インポート（`from . import xxx`）は使用禁止。
  - 理由: スクリプトとして直接実行（`__main__`）された際に `ImportError` を引き起こすため。
- **例**:
  - ✅ `from module.utils import data_loader`
  - ❌ `from .utils import data_loader`

### 2. Modification Safety
インポート文を変更した際は、必ず**実行確認**を行ってください。静的解析（Lint）でエラーが出なくても、実行時の `sys.path` 設定によっては `ModuleNotFoundError` になる可能性があります。
---

## 📖 Docstrings

- **適用範囲**: 全ての関数、メソッド、クラス。
- **スタイル**: Google Style Guide 準拠。
- **言語**: 日本語。
- **フォーマット**: 72文字で改行し、インデントを揃える。

### 再現実装時のソース明記
Kaggle Notebookや外部コードの再現実装を行う場合は、**スクリプトのモジュールdocstring**に以下の情報を必ず記載すること：
- **再現対象**: 何を再現しているか（Notebook名、LBスコア等）
- **参考ソース**: `reference/` 配下のファイルパス

```python
"""ByT5ベースライン学習スクリプト.

dpc-starter-train（LB 26.8）の再現を目的とする。
参考: reference/notebooks/dpc-starter-train_claude.py
"""
```

これにより、実装の出典が明確になり、後から参照・検証が容易になる。

### Template Example
```python
def compute_average(values: list[float]) -> float:
    """
    Compute the arithmetic mean of a list of floats.
    (1行目は関数の目的を簡潔に書く)

    Args:
        values (list[float]): 平均を計算する対象の数値リスト
                              ([A, B]のようにデータの意味を具体的に記述)

    Returns:
        float: リスト内の数値の算術平均

    Raises:
        ValueError: `values` が空リストの場合
    """
    if not values:
        raise ValueError("values must not be empty")
    return sum(values) / len(values)

```

## 📊 Visualization
- 言語: タイトル、軸ラベル、凡例はすべて 英語 とする。

- 視認性:
  - 文字サイズ（フォント）や数値を大きく設定する。
  - 凡例（Legend）がプロット等の重要な情報に被らないように配置を調整する。

## 📓 Jupyter Notebook Workflow
Notebook (.ipynb) は直接編集・コミットせず、以下のフローで作業を行ってください。

1. 変換: 作業前に .py ファイルに変換する。

```bash
jupyter nbconvert --to script <file.ipynb> --output <file_claude.py>
# 注意: 拡張子が .py.py にならないように注意
```
2. 編集: 変換された .py ファイル上でコード修正やコミットを行う。
