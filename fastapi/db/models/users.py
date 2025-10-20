from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator

from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, selectinload

from .base import Base


# ----------------------------------------------------
# 投稿（User）テーブルの定義
# ----------------------------------------------------
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        "id",
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column("name", String(length=40), nullable=False)

    # 全件取得
    @classmethod
    async def read_all(cls, session: AsyncSession) -> AsyncIterator[User]:
        stmt = select(cls)
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    # idから取得
    @classmethod
    async def read_by_id(cls, session: AsyncSession, user_id: int) -> User | None:
        stmt = select(cls).where(cls.id == user_id)
        return await session.scalar(stmt)

    # 1件登録
    @classmethod
    async def create(cls, session: AsyncSession, name: str) -> User:
        user = User(
            name=name,
        )
        session.add(user)
        await session.flush()  # DBに実際のINSERT文を送ってid生成
        new = await cls.read_by_id(
            session,
            user.id,
        )
        if not new:
            raise RuntimeError()
        return new

    # 1件に対し更新
    async def update(self, session: AsyncSession, name: str) -> None:
        self.name = name
        await session.flush()

    # 1件削除
    @classmethod
    async def delete(cls, session: AsyncSession, user: User) -> None:
        await session.delete(user)
        await session.flush()
