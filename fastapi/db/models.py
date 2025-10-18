from sqlalchemy import Column, String, Integer

from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


# ----------------------------------------------------
# 投稿（User）テーブルの定義
# ----------------------------------------------------
class User(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
