# fast_api_practice

## 1. APIの種類
- [なろう仕様書リポジトリ](https://github.com/watame/mobile_web_novel_reader)

## 2. 開発環境構築

### 環境変数の設定

開発環境をセットアップする前に、以下の環境変数を設定する必要があります。`.env` ファイルをプロジェクトのルートディレクトリに作成し、以下の内容を追加してください。

| 環境変数名          | 説明                   | ローカルでの推奨値        |
|-------------------|----------------------|-------------------------|
| `POSTGRES_NAME`   | Postgresのデータベース名 | `postgres`              |
| `POSTGRES_USER`   | Postgresのユーザー名    | `postgres`              |
| `POSTGRES_PASSWORD` | Postgresのパスワード    | `postgres`              |
| `POSTGRES_HOST`   | Postgresのホスト名     | `db`                    |
| `POSTGRES_PORT`   | Postgresのポート番号    | `5432`                  |
| `JWT_SECRET_KEY`  | JWTの秘密鍵             | `8ae240d39...376193c6`  |

### コンテナの操作

1. イメージの作成

以下コマンドで Docker image を作成します。ファイルは開発用の docker-compose.yml を指定します。
"""
make build
"""

2. コンテナの起動

以下のコマンドでコンテナを起動します。

"""
make up
"""

3. 動作確認

http://localhost:8000 にアクセスし、Swaggerの画面が出たら成功です。

### コンテナの停止

以下のコマンドでコンテナを停止します。
"""
make down
"""

### マイグレーション

#### マイグレーションファイルを作成する
"""
poetry run alembic revision --autogenerate
"""

#### マイグレーションを実行する

"""
poetry run alembic upgrade head
"""

