#!/bin/sh
set -e

# DBが起動するまで待機
echo "Waiting for DB..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
echo "DB is up!"

cd /app/fastapi

echo "Running Alembic migrations..."
alembic upgrade head

# コンテナ起動時に実行
# "main:app"の部分は、FastAPIインスタンスが定義されている実際のモジュールと変数名に置換
# --reload :開発時のホットリロードを有効
# ※※※Todo:本番環境では --reload を削除
# FastAPI 起動
echo "Starting FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload