---
name: sync-progress
description: Obsidianから進捗.mdを同期してprogressファイルを更新
---

# 進捗同期 & Progress更新

Obsidianの進捗.mdをGitHubから取得し、progressファイル群を更新する。

## 手順

### Step 1: 進捗.mdの同期
```bash
bash scripts/sync_obsidian_progress.sh
```
を実行してGitHubから最新の `reference/progress/進捗.md` を取得する。

### Step 2: 差分の特定
以下の4ファイルをすべて読み込む：
- `reference/progress/進捗.md`（同期後の最新版）
- `reference/progress/experiment_log.md`
- `reference/progress/dashboard.md`
- `reference/progress/plan.md`

進捗.mdの内容のうち、experiment_log/dashboard/planに**まだ反映されていない情報**を特定する。
差分がない場合は「progressは最新です」と報告して終了。

### Step 3: progressファイルの更新
差分がある場合、以下のルールに従って更新する。

#### experiment_log.md
- 新しい実験があれば、テーブルに行を追加する
- IDは連番（最後のIDの次）
- 結果記号の基準: `++`(+2以上), `+`(+0.5〜2), `=`(±0.5), `-`(-0.5〜-2), `--`(-2以下)
- 新たな知見があれば「判明した知見」セクションに追記

#### dashboard.md
- CVまたはLBのベストスコアが更新された場合、テーブルを更新
- 結論が確定した知見があれば追記

#### plan.md
- 完了した計画は ✅ マークを付ける
- 新しい計画や優先順位の変更があれば反映
- 新たな確定知見があれば追記

### Step 4: 差分サマリーの報告
更新した内容を簡潔に報告する。形式：
```
**更新内容:**
- experiment_log: E0XX追加（内容の要約）
- dashboard: ベストCV更新 XX.XX
- plan: XXを完了に更新
```
