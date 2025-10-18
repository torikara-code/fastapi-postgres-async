# Debianベースの軽量なPythonイメージを使用
FROM python:3.12-slim

# 作業ディレクトリをコンテナ内に設定
WORKDIR /app

# requirements.txtファイルをコンテナの/appディレクトリにコピー
COPY requirements.txt .

# システム依存関係のインストールとPythonパッケージのインストール
# slim (Debian) 環境でのC拡張ビルドに必要なパッケージをインストール
# - gcc, g++: C/C++ コンパイラ (ビルドツールチェーン)
# - libpq-dev: PostgreSQLライブラリの開発ファイル
# - python3-dev: Pythonのヘッダーファイル
# インストール後に不要になったaptのキャッシュを削除し、イメージサイズを小さく保持
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  libpq-dev \
  python3-dev \
  && pip install --upgrade pip

# Python依存関係をインストール
# extras ([email], [cryptography]) を明示的に指定
RUN pip install --no-cache-dir -r requirements.txt \
  pydantic[email]==2.6.0 \
  python-jose[cryptography]==3.3.0

# ビルド時にインストールしたシステムパッケージはランタイムでは不要、削除してイメージサイズを最適化
# libpq5 (libpq-devのランタイム部分) は残し、それ以外を削除
RUN apt-get purge -y --auto-remove build-essential libpq-dev python3-dev \
  && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# アプリケーションコードのコピー
# ------------------------------------------------------------------

COPY . /app

# ------------------------------------------------------------------
# ポートと起動コマンド (FastAPI/Uvicorn用)
# ------------------------------------------------------------------

# Uvicornがデフォルトで使用するポートを公開
EXPOSE 8000

# コンテナ起動時に実行
# "main:app"の部分は、FastAPIインスタンスが定義されている実際のモジュールと変数名に置換
# --reload :開発時のホットリロードを有効
# ※※※Todo:本番環境では --reload を削除
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]