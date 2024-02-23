# fast_api_practice

## 1. APIの種類
- [なろう仕様書リポジトリ](https://github.com/watame/mobile_web_novel_reader)

## 2. 開発環境構築

1. イメージの作成

以下コマンドで Docker image を作成します。ファイルは開発用の docker-compose.yml を指定します

```
make build
```

2. コンテナの起動

以下のコマンドでコンテナを起動します

```
make up
```

3. 動作確認

http://localhost:8000 にアクセスし、Swaggerの画面が出たら成功です


### コンテナの停止

以下のコマンドでコンテナを停止します

```
make down
```

#### マイグレーションファイルを作成する
※ -m 以下の文言は自由です
```
poetry run alembic revision --autogenerate -m "create tables"
```

#### マイグレーションを実行する
```
poetry run alembic upgrade head
```