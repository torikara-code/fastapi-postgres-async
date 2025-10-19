from pydantic_settings import BaseSettings, SettingsConfigDict


# BaseSettingsを継承して、環境変数を自動的に読み込む
class Settings(BaseSettings):
    # .envファイルや環境変数から読み込む際のプレフィックス
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # アプリケーション設定
    APP_NAME: str = "FastAPI App"

    # データベース接続設定 (docker-compose.ymlのenvironmentと一致させる)
    POSTGRES_PORT: int
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # SQLAlchemyで使用する接続URLをプロパティで定義
    @property
    def database_url(self) -> str:
        # FastAPIアプリケーションのメイン接続 (asyncpg: 非同期ドライバを使用するための形式)
        url = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return url

    @property
    def database_url_sync(self) -> str:
        # psycopg2 (同期ドライバ) を使用するための形式（Alembicの同期デバッグ時などに使用）
        url = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return url

# グローバル変数に保持
settings = Settings.model_validate({})