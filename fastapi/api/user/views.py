from fastapi import APIRouter, Depends, Path, Request

from db.models import UserSchema

from .schema import (
    CreateUserRequest,
    CreateUserResponse,
    ReadAllUserResponse,
    ReadUserResponse,
    UpdateUserRequest,
    UpdateUserResponse,
)

from .use_cases import CreateUser, DeleteUser, ReadAllUser, ReadUser, UpdateUser

router = APIRouter(prefix="/user")


# 一件登録API
@router.post("", response_model=CreateUserResponse)
async def create(
    request: Request,
    data: CreateUserRequest,
    use_case: CreateUser = Depends(CreateUser),
) -> UserSchema:
    return await use_case.execute(data.name)


# 全件取得API
@router.get("", response_model=ReadAllUserResponse)
async def read_all(
    request: Request,
    use_case: ReadAllUser = Depends(ReadAllUser),
) -> ReadAllUserResponse:
    return ReadAllUserResponse(users=[user async for user in use_case.execute()])


# id指定一件取得API
@router.get("/{user_id}", response_model=ReadUserResponse)
async def read(
    request: Request,
    user_id: int = Path(..., description="取得対象のユーザid"),
    use_case: ReadUser = Depends(ReadUser),
) -> UserSchema:
    return await use_case.execute(user_id)


# id指定一件更新API
@router.put("/{user_id}", response_model=UpdateUserResponse)
async def update(
    request: Request,
    data: UpdateUserRequest,
    user_id: int = Path(..., description="更新対象のユーザID"),
    use_case: UpdateUser = Depends(UpdateUser),
) -> UserSchema:
    return await use_case.execute(user_id, data.name)


# id指定削除API
@router.delete("/{note_id}", status_code=204)
async def delete(
    request: Request,
    note_id: int = Path(..., description="削除対象のユーザID"),
    use_case: DeleteUser = Depends(DeleteUser),
) -> None:
    await use_case.execute(note_id)
