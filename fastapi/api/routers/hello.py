from fastapi import APIRouter

from fastapi import Form, HTTPException, APIRouter
from typing import Dict, Any
from db.models.users import User
from db.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()


@router.get("/hello")
async def say_hello_url_parameter(name: str) -> Dict[str, str]:
    # ユーザーが要求したurlパラメータ 'name' の値を返却
    return {"return_value": name}


@router.get("/hello/{name}")
async def say_hello_path(name: str) -> Dict[str, str]:
    # ユーザーが要求したパスパラメータ 'name' の値を返却
    return {"return_value": name}


@router.post("/regist_name")
async def receive_name_from_form(
    name: str = Form(...),
) -> Dict[str, Any]:
    try:
        async with AsyncSession() as session:
            async with session.begin():
                # ID を指定せずに追加 → 自動連番
                new_user = User(name=name)
                session.add(new_user)
            # commit は context manager の `session.begin()` で自動
            await session.refresh(new_user)  # 新しい ID を取得

            return {"id": new_user.id, "name": new_user.name}

    except SQLAlchemyError as e:
        # DB関連のエラーをキャッチして返す
        # e.__str__() で詳細メッセージを取得できる
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        # 予期しないその他のエラー
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
