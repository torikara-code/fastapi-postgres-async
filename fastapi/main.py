from typing import Dict, Any
from fastapi import FastAPI, Form, HTTPException
import uvicorn
from db.models import User
from db.session import async_session
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import text


app = FastAPI(title="FastAPI REST API", description="A REST API", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello")
async def say_hello(name: str) -> Dict[str, str]:
    # ユーザーが要求した通り、パスパラメータ 'name' の値を返却
    return {"return_value": name}


@app.get("/hello/{name}")
async def say_hello(name: str) -> Dict[str, str]:
    # ユーザーが要求した通り、パスパラメータ 'name' の値を返却
    return {"return_value": name}


@app.post("/receive_name")
async def receive_name_from_form(
    name: str = Form(...),
) -> Dict[str, Any]:
    try:
        async with async_session() as session:
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
