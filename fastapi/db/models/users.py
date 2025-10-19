from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


# ----------------------------------------------------
# 投稿（User）テーブルの定義
# ----------------------------------------------------
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True,
    )
    name: Mapped[str] = mapped_column("name", String(length=40), nullable=False)
