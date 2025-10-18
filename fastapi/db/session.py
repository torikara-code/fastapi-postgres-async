from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from settings import Settings

settings_instance = Settings()
database_url = settings_instance.database_url

# 非同期エンジンを作成
engine = create_async_engine(database_url, echo=True, future=True)

# 非同期セッションを生成するファクトリ
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
