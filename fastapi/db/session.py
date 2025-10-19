import logging
from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from settings import settings

logger = logging.getLogger(__name__)

# 非同期エンジンを作成
async_engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=False,
)


# 非同期セッションを生成するファクトリ
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as e:
        logger.exception(e)


AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]
