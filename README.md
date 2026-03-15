# Book Management API

FastAPI + AWS Lambda（コンテナ）+ DynamoDB による本の管理 API です。

## 技術スタック

| 項目 | 技術 |
|------|------|
| フレームワーク | FastAPI |
| Lambda アダプター | Mangum |
| データベース | Amazon DynamoDB |
| IaC | Terraform |
| コンテナ | Docker（マルチステージビルド） |
| CI | GitHub Actions |

## ディレクトリ構成

```
.
├── src/
│   ├── main.py          # FastAPI アプリ・Lambda ハンドラー
│   ├── models.py        # Pydantic モデル
│   ├── database.py      # DynamoDB 操作
│   └── routers/
│       └── books.py     # CRUD エンドポイント
├── tests/               # pytest テスト
├── scripts/
│   └── create_table.py  # ローカル用テーブル作成
├── Dockerfile           # マルチステージビルド
├── docker-compose.yml   # DynamoDB Local
└── Makefile
```

## API エンドポイント

| メソッド | パス | 説明 |
|--------|------|------|
| `GET` | `/health` | ヘルスチェック |
| `POST` | `/books` | 本を登録 |
| `GET` | `/books` | 一覧取得 |
| `GET` | `/books/{id}` | 1 件取得 |
| `PATCH` | `/books/{id}` | 部分更新 |
| `DELETE` | `/books/{id}` | 削除 |

一覧取得はクエリパラメータ `limit`（1〜100、デフォルト 20）と `last_key` によるページネーションに対応しています。

## ローカル開発

**前提条件:** Python 3.12、Docker

```bash
# 依存パッケージのインストール
make install-dev

# DynamoDB Local + FastAPI 起動
make local
```

起動後は http://localhost:8080 でアクセスできます。Swagger UI は http://localhost:8080/docs です。

```bash
# 停止
make local-stop
```

## テスト

```bash
make test
```

## Makefile ターゲット一覧

```
make help
```
