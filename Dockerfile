# Debianベースのpythonイメージ
FROM python:3.12-slim

# 作業ディレクトリをコンテナ内に設定
WORKDIR /app

# requirements.txtファイルをコンテナの/appディレクトリにコピー
COPY requirements.txt .

# システム依存関係のインストールとPythonパッケージのインストール
# --no-install-recommends → 依存関係のうち必須でないパッケージは入れない
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  libpq-dev \
  python3-dev \
  postgresql-client \
  && pip install --upgrade pip

# Python依存関係をインストール
# extras ([email], [cryptography]) を明示的に指定
RUN pip install --no-cache-dir -r requirements.txt \
  pydantic[email]==2.6.0 \
  python-jose[cryptography]==3.3.0

# ビルド時にインストールしたシステムパッケージはランタイムでは不要、削除してイメージサイズを最適化
# libpq-devは残し、それ以外を削除
RUN apt-get purge -y --auto-remove build-essential libpq-dev python3-dev \
  && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# アプリケーションコードのコピー
# ------------------------------------------------------------------

COPY fastapi/ /app/fastapi/
COPY config/entrypoint.sh /app/config/entrypoint.sh
RUN chmod +x /app/config/entrypoint.sh

# ------------------------------------------------------------------
# ポートと起動コマンド (FastAPI/Uvicorn用)
# ------------------------------------------------------------------

# Uvicornがデフォルトで使用するポートを公開
EXPOSE 8000

ENTRYPOINT ["/app/config/entrypoint.sh"]