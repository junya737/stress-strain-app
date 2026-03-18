# CLAUDE.md
This file provides guidance to Claude Code.

## CRITICAL META-RULES
- **Language**: 回答は常に**日本語**で行ってください。
- **Rule Source**: 詳細な手順は必ず後述の **Rule Index** 内の各ファイルに従ってください。

## YOU MUST
- **Virtual Env**: 作業前に必ず仮想環境を有効化してください（Base環境の使用は**絶対禁止**）。
- **Branch Strategy**: `main` ブランチでの作業は禁止です。必ず作業用ブランチを作成・移動してから修正を行ってください。
- **Standard Process**: `.claude/rules/workflow.md` の手順を厳守してください。
- **Root Execution**: スクリプトは必ずプロジェクトルートから実行してください。
  - Correct: `python scripts/filename.py`

## YOU NEVER
- **No Secrets**: パスワードやAPIキーをハードコーディングしないこと。
- **No Unauthorized Deletion**: ユーザーの確認なしにデータを削除しないこと。
- **No Unauthorized Install**: 許可なくライブラリやパッケージをインストールしないこと（`rules/permissions.md` 参照）。
- **No Untested Deploy**: テストなしで本番環境にデプロイしないこと。
- **No Main Commit**: `main` ブランチに直接コミットしないこと。
- **No Data Edit**: `data/raw/` および `data/processed/` 内のファイルは直接編集しないこと。

## Rule Index
詳細なルールは以下のファイルを参照してください。

| Category | File |
| :--- | :--- |
| **Project Info** | `.claude/rules/project-info.md` |
| **Workflow & Git** | `.claude/rules/workflow.md` |
| **Permissions** | `.claude/rules/permissions.md` |
| **Python Coding** | `.claude/rules/python-coding.md` |
| **Environment** | `.claude/rules/environment.md` |
| **Testing** | `.claude/rules/testing-guidlines.md` |
| **CI/CD** | `.claude/rules/github-actions.md` |
| **Kaggle Operations** | `.claude/rules/kaggle/operations.md` |
| **Kaggle Competition Info** | `.claude/rules/kaggle/competition-info/*.md` |
| **Knowledge Management** | `.claude/rules/knowledge-management.md` |
| **Progress Tracking** | `.claude/rules/progress-tracking.md` |
| **Multi-Agent** | `.claude/rules/multi-agent.md` |

## Skills（必要時に `/skill-name` で呼び出し）
| Skill | 説明 |
| :--- | :--- |
| `/summarize-discussion` | Kaggleディスカッションのまとめ作成 |
| `/summarize-notebook` | Kaggleノートブックのまとめ作成 |
| `/summarize-strategy` | Kaggle戦略のまとめ作成 |
| `/hpc-helper` | 九大Genkaiスパコン操作ガイド |
| `/create-experiment` | バッチ実験スクリプト（bash）の作成ガイド |

