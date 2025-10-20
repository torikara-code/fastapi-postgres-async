from pydantic import BaseModel, Field

from db.models import UserSchema


# 新しいユーザ登録
class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=40)


# ユーザ登録時のレスポンス受信
class CreateUserResponse(UserSchema):
    pass


# 一件select
class ReadUserResponse(UserSchema):
    pass


# 全件select
class ReadAllUserResponse(BaseModel):
    users: list[UserSchema]


# 更新用スキーマ
class UpdateUserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=40)


# 更新時のレスポンス受信
class UpdateUserResponse(UserSchema):
    pass
