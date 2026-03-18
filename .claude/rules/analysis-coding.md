# Analysis & EDA Coding Guidelines

## 定数
- **定義場所**: `analysis/constants.py`
- **使用方法**: 各スクリプトでインポートして使用

```python
import sys
from pathlib import Path

# プロジェクトルートをsys.pathに追加（Notebook実行時用）
_project_root = str(Path(__file__).resolve().parent.parent) if "__file__" in dir() else str(Path.cwd().parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from analysis.constants import RAW_DIR

# プロジェクトルートを基準に絶対パスを構築
RAW_DIR = f"{_project_root}/{RAW_DIR}"
```

## 図の保存
- **デフォルトでは保存しない** - `plt.show()` のみ使用
- **ユーザーから明示的に依頼された場合のみ** `save_fig()` を追加する
- 保存先: `data/figure/{script_name}/`

## 図のスタイル規約

### 軸ラベル（必須）
- **x軸・y軸には必ずラベルを設定すること**（`ax.set_xlabel()`, `ax.set_ylabel()`）
- ラベルなしのプロットは禁止

### 共通フォント設定
- スクリプト冒頭で `plt.rcParams.update()` を使い、大きめのフォントサイズを一括設定すること
- 以下を標準設定として使用する：

```python
plt.rcParams.update(
    {
        "font.size": 18,
        "axes.titlesize": 18,
        "axes.labelsize": 18,
        "xtick.labelsize": 18,
        "ytick.labelsize": 18,
        "legend.fontsize": 18,
        "figure.dpi": 100,
    }
)
```

### グリッド
- **y軸方向のグリッドを必ず表示すること**
- `ax.yaxis.grid(True, alpha=0.3)` と `ax.set_axisbelow(True)` を設定する
- x軸方向のグリッドはデフォルトでは不要（棒グラフ等では邪魔になるため）

## Notebook互換のためのルール

スクリプト全体を1セルにコピペして動作させるため、以下を守ること：

1. **`matplotlib.use("Agg")` 禁止** - インライン表示が無効になるため
2. **`plt.show()` を使用** - 各図の後に呼び出す
3. **`plt.close()` は使わない** - Notebookで図が表示されなくなる
4. **`argparse` 禁止** - Notebookの引数と競合するため。EDAにdebugモード等は不要
5. **パスは絶対パスで構築** - `_project_root` を基準にすることでNotebookでも動作する

## コード例

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/raw/train.csv")

# 図1
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df["column"], bins=50)
ax.set_title("Distribution")
plt.show()

# 図2
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df["x"], df["y"])
plt.show()
```

## 図の保存を依頼された場合

ユーザーから依頼があった場合のみ、以下の `save_fig()` を追加する：

```python
FIG_DIR = f"{_project_root}/data/figure/eda_train"

def save_fig(fig, name):
    Path(FIG_DIR).mkdir(parents=True, exist_ok=True)
    fig.savefig(f"{FIG_DIR}/{name}.png", dpi=150, bbox_inches="tight")
```
