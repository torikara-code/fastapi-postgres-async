# 環境設定テンプレート(.env)

```
# アプリケーションの動作モード (development, staging, production)
ENV=development

# データベース接続情報: 各自の環境で適切なパスワード、ホストを設定
POSTGRES_USER=user_name
POSTGRES_PASSWORD=
POSTGRES_DB=db_name
POSTGRES_HOST=host_db_name

# ポート情報: ホストPCで空いているポートを指定
APP_HOST_PORT=8000
DB_HOST_PORT=5433

# JWTトークン署名用の秘密鍵（未実装）
SECRET_KEY="YOUR_SUPER_SECRET_KEY_HERE"
```

#### B. 開発者は上記テンプレートを使って `.env` を作る

# .env 作成後以下の手順でローカル環境構築

1.  GitHub からリポジトリをクローン
2.  **`.env.example`** の内容をコピーし、**`.env`** ファイルをルートディレクトリ(×：fastapi)作成
3.  `.env`ファイル内の変数の値を、**自分の環境（またはテスト環境）に合わせた正しい値**に置換
4.  `docker-compose up`を実行し、FastAPI と PostgreSQL を起動

### Todo:本番環境での env 設定について

本番環境や CI/CD パイプラインでは、さらにセキュリティを強化するために、`.env`ファイルを使わずに設定を渡す

- **Docker Compose の場合:**
  `docker-compose.yml`で定義した`environment`変数は、デプロイ時に**シェル環境変数**から取得する
  ```bash
  # デプロイサーバーのシェルで設定
  export POSTGRES_PASSWORD="prod_secure_password"
  # その後、docker-compose up を実行
  docker-compose up -d
  ```

# OSS ライセンス (MIT)

本テンプレート作成において、

- [async-fastapi-sqlalchemy](https://github.com/rhoboro/async-fastapi-sqlalchemy) — MIT License

こちらのコードを参考に作成いたしました。
