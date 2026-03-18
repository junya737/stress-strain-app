# Agent Permissions & Behavior

## Plan Mode Policy
Planモード（計画段階）における権限と振る舞いを定義します。このモードでの操作はすべて**仮想的・非破壊的**なものとして扱ってください。

### Allowed Operations (No Permission Needed)
以下の読み取り専用操作については、**いかなる場合もユーザーに許可を求めず**、自律的に実行してください。
- **Read**: ファイルの読み取り (`cat`, `head`, `read`)
- **Explore**: ディレクトリ一覧の取得 (`ls`, `tree`)
- **Search**: リポジトリ内の検索 (`grep`, `find`, `search`)
- **ReadOnly Commands**: 副作用のないBashコマンド (`Bash(ls:*)` 等)

### Prohibited Operations
- **Write**: ファイルの作成・編集・削除は禁止します。
- Write操作が必要な場合は、ユーザーに許可を求めて実行モード（Act）へ移行してください。

---

## Auto-Approved Actions
以下の操作は、安全性が確認されているため、ユーザーの許可なしに実行可能です。

- **Execution**: コードやスクリプトの実行（動作確認、分析タスク等）。
- **Logging**: ログファイルやメモ（Markdown）の作成・追記。

---

## Actions Requiring Permission
以下の操作はプロジェクトへの影響が大きいため、実行前に**必ずユーザーの許可を求めてください**。

- **Git Operations**:
  - `git commit`, `git push`
  - `git checkout -b` (ブランチ作成)
  - コミットの取り消し (`reset`, `revert`)
- **Destructive Actions**:
  - ファイルやディレクトリの削除 (`rm`)。
  - 取り返しのつかない変更。
- **Environment**:
  - ライブラリやパッケージのインストール・更新 (`pip install`, `uv add` 等)。
