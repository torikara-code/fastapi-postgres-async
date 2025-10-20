from typing import AsyncIterator

from fastapi import HTTPException

from db.session import AsyncSession
from db.models import User, UserSchema


# ユーザ作成
class CreateUser:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, name: str) -> UserSchema:
        async with self.async_session.begin() as session:
            user = await User.create(session, name)
            return UserSchema.model_validate(user)


# ユーザ全件読み込み
class ReadAllUser:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self) -> AsyncIterator[UserSchema]:
        async with self.async_session() as session:
            async for user in User.read_all(session):
                yield UserSchema.model_validate(user)


# id指定ユーザ読み込み
class ReadUser:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, user_id: int) -> UserSchema:
        async with self.async_session() as session:
            user = await User.read_by_id(session, user_id)
            if not user:
                raise HTTPException(status_code=404)
            return UserSchema.model_validate(user)  # DB形式からpydantic形式に変換


# id指定ユーザ更新
class UpdateUser:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, user_id: int, name: str) -> UserSchema:
        async with self.async_session.begin() as session:
            user = await User.read_by_id(session, user_id)
            if not user:
                raise HTTPException(status_code=404)

            await user.update(session, name)
            await session.refresh(user)
            return UserSchema.model_validate(user)


# id指定ユーザ削除
class DeleteUser:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, user_id: int) -> None:
        async with self.async_session.begin() as session:
            user = await User.read_by_id(session, user_id)
            if not user:
                return
            await User.delete(session, user)
