#!/bin/bash

set -eu

# マイグレーションを実行
echo "Running migrations..."
poetry run alembic revision --autogenerate
poetry run alembic upgrade head

# アプリケーションを起動
echo "Starting the application..."
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000