# テストコード作成ガイドライン

## 基本方針
- **フレームワーク**: pytest（`pytest tests/ -v`）
- **命名**: `test_{対象ファイル名}.py`
- **配置**: `tests/` ディレクトリ
- **独立性**: 各テストは他テストに依存せず、実行順序不問
- **クリーンアップ**: 作成したファイル・ディレクトリは必ず後始末（`tempfile`、`with`文活用）

## テストの種類
1. **再現性テスト**: 同一seed・同一入力で同一出力を確認
2. **ユニットテスト**: 個々の関数の入出力を検証
3. **統合テスト**: 複数コンポーネントのE2Eフロー検証

## 実行
```bash
pytest tests/test_xxx.py -v          # 特定ファイル
pytest tests/test_xxx.py::test_func  # 特定関数
pytest -k "keyword" -v               # キーワードフィルタ
pytest -s --tb=long                  # 標準出力表示＋詳細トレースバック
```

## 注意事項
- プロジェクトルートから実行を前提とする
- 長時間テストには `@pytest.mark.slow` を付与（CIで `pytest -m "not slow"` で除外可能）
