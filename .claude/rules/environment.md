# Environment & Package Management

このドキュメントは、Python仮想環境の取り扱いとパッケージ管理ツールに関するルールを定義します。

## 🛠 Core Policy
- **Manager**: パッケージ管理には **`uv`** を使用する。
- **Base Image**: Kaggleコンテナ環境をベースとしている。
- **Strict Rule**: システムPython (`/usr/bin/python` 等) の使用は**絶対禁止**。必ず以下の手順で仮想環境を有効化してから作業を行うこと。

## 🔌 Activation Rules 

```bash
uv run python3 scripts/your_script.py
```

## 📦 Package Operations
Add: パッケージ追加は `uv add <package> --python .venv` を使用する。ベース環境（Kaggleコンテナ）に影響を与えないよう、必ず `--python .venv` を指定すること。実行前に permissions.md に従い許可を求めること。

Sync: uv sync

Deactivate: 作業終了時や環境を切り替える際は deactivate を実行する。

## 🔍 Library Verification
本プロジェクトはKaggleコンテナをベース環境とし、その上に uv の `.venv` を重ねている。
`pyproject.toml` の dependencies にはプロジェクト固有の追加パッケージしか記載されない。

ライブラリの有無を確認する際は、以下の2つを区別して確認すること:

- **ベース環境（Kaggleコンテナ）**: `pip list | grep <pkg>`
- **仮想環境（.venv、uv管理）**: `pip --python .venv/bin/python list | grep <pkg>`

新規パッケージが必要な場合のみ `uv add` で追加する。ベースに既存のパッケージを重複追加しないこと。
**インストール実行前には必ずユーザーの許可を得ること。**
