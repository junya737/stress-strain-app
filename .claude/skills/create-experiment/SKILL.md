---
name: create-experiment
description: バッチ実験スクリプト（bash）の作成ガイド
---

# バッチ実験スクリプトの作成方法

実験をbashスクリプトで一括実行するためのガイド。

## 保存場所・命名規則

| 項目 | パス |
|------|------|
| スクリプト | `experiments/run_exp{NNN}_{name}.sh` |
| ログ出力 | `data/exp_logs/<JST timestamp>/` |

- 番号 `{NNN}` は `experiments/` 内の既存スクリプトから連番で採番
- ログディレクトリは実行時にJST時刻（`YYYYMMDD_HHMM`）で自動生成

## 実行方法

```bash
# 通常実行
bash experiments/run_exp002_hparam_sweep.sh

# debugモード（各実験に -d フラグを付与）
DEBUG=1 bash experiments/run_exp002_hparam_sweep.sh
```

## train_byt5.py の CLI引数

| 引数 | 短縮 | 説明 | 例 |
|------|------|------|-----|
| `--model` | `-m` | モデル選択 | `-m byt5-base`, `-m byt5-large` |
| `--debug` | `-d` | debugモード（少量データで高速確認） | `-d` |
| `--override` | `-o` | Config値の上書き（複数指定可） | `-o model.epochs=20 model.label_smoothing=0.1` |
| `--run-name` | — | 出力ディレクトリの名前プレフィックス | `--run-name base_ls01` |
| `--no-bidirectional` | — | 双方向学習を無効化 | `--no-bidirectional` |

### override で指定できるフィールド

```
# model.* （ByT5BaseConfig / ByT5LargeConfig のフィールド）
model.epochs=30
model.learning_rate=1e-4
model.label_smoothing=0.2
model.weight_decay=0.01
model.dropout_rate=0.1
model.batch_size=16
model.num_beams=1
model.lr_scheduler_type=cosine
model.warmup_ratio=0.1
model.use_bf16=true
model.gradient_accumulation_steps=2
model.gradient_checkpointing=true

# augmentation.*
augmentation.enabled=true
augmentation.replace_prob=0.5

# トップレベル
seed=123
```

## テンプレート

```bash
#!/bin/bash
# 一括実験実行スクリプト
#
# 使い方:
#   bash experiments/run_expXXX_name.sh
#   DEBUG=1 bash experiments/run_expXXX_name.sh  # debugモード
#
# 各実験は独立して実行され、失敗しても次の実験に進む。
# ログは data/exp_logs/<JST timestamp>/ に保存される。

set -o pipefail

SCRIPT_PATH="$(readlink -f "$0")"
BATCH_START=$(TZ=Asia/Tokyo date '+%Y%m%d_%H%M')
LOG_DIR="data/exp_logs/${BATCH_START}"
mkdir -p "$LOG_DIR"

# スクリプト自身をログディレクトリにコピー（再現性のため）
cp "$SCRIPT_PATH" "$LOG_DIR/"

BATCH_LOG="$LOG_DIR/batch.log"

# debugモード: DEBUG=1 で実行すると各実験に -d フラグを付与
DEBUG_FLAG=""
if [ "${DEBUG:-0}" = "1" ]; then
    DEBUG_FLAG="-d"
fi

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg" | tee -a "$BATCH_LOG"
}

run_experiment() {
    local name="$1"
    shift
    local log_file="$LOG_DIR/${name}.log"

    log "=== START: $name ==="
    log "Command: $*"
    log "Log file: $log_file"

    local start_ts=$(date +%s)
    uv run "$@" > "$log_file" 2>&1
    local exit_code=$?
    local end_ts=$(date +%s)
    local elapsed=$(( end_ts - start_ts ))
    local hours=$(( elapsed / 3600 ))
    local minutes=$(( (elapsed % 3600) / 60 ))
    local seconds=$(( elapsed % 60 ))

    if [ $exit_code -eq 0 ]; then
        log "=== DONE: $name (${hours}h${minutes}m${seconds}s) ==="
    else
        log "=== FAIL: $name (exit=$exit_code, ${hours}h${minutes}m${seconds}s) ==="
    fi
    log ""
    return $exit_code
}

if [ -n "$DEBUG_FLAG" ]; then
    log "Batch experiments started at $BATCH_START [DEBUG MODE]"
else
    log "Batch experiments started at $BATCH_START"
fi
log ""

# --- 実験定義 ---
# ここに実験を追加する

log "All experiments finished."
```

## 実験定義の書き方

```bash
# パターン1: モデル切り替え
run_experiment "large_base" \
    python3 scripts/train_byt5.py -m byt5-large $DEBUG_FLAG \
    --run-name large_base

# パターン2: ハイパーパラメータ変更（単一）
run_experiment "base_ls01" \
    python3 scripts/train_byt5.py -m byt5-base $DEBUG_FLAG \
    --run-name base_ls01 \
    -o model.label_smoothing=0.1

# パターン3: 複数パラメータ同時変更
run_experiment "base_ep20_ls01" \
    python3 scripts/train_byt5.py -m byt5-base $DEBUG_FLAG \
    --run-name base_ep20_ls01 \
    -o model.epochs=20 model.label_smoothing=0.1

# パターン4: augmentation有効化
run_experiment "base_pn_aug" \
    python3 scripts/train_byt5.py -m byt5-base $DEBUG_FLAG \
    --run-name base_pn_aug \
    -o augmentation.enabled=true
```

## 注意事項

- `--run-name` に日付サフィックスは不要（train_byt5.pyがJSTタイムスタンプを自動付与）
- `$DEBUG_FLAG` は必ず各実験コマンドに含めること
- 実行前に `DEBUG=1` で全実験が正常終了することを確認すること
- 実行はプロジェクトルートから行うこと
