# ------------------------------------------------
# 標準ライブラリ
# ------------------------------------------------
import os  # operate filepath, read env etc...
import sys
import asyncio  # async func

# ログ出力
from logging.config import fileConfig

# ------------------------------------------------
# サードパーティライブラリ
# ------------------------------------------------
from dotenv import load_dotenv  # .env ファイルから環境変数を読み込む
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config  # 非同期接続DBエンジン
from alembic import context  # migration tool alembic

# ------------------------------------------------
# グローバル設定
# ------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # fastapi

# ------------------------------------------------
# モデルのインポート
# ------------------------------------------------
from db.models.base import Base

from settings import settings
from db.session import async_engine


# .envファイルを読み込み
load_dotenv(dotenv_path=os.path.join(PROJECT_ROOT, ".env"))

# ------------------------------------------------
# Alembic初期設定
# ------------------------------------------------

# Alembic Configオブジェクト（設定情報を格納）
config = context.config

# Alembicの接続先DB情報設定
config.set_main_option("sqlalchemy.url", settings.database_url)

# ロギング設定
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata設定：最新のデータベース設計図（DBとの差分）
target_metadata = Base.metadata


def include_object(obj, name, type_, reflected, compare_to):
    if obj.info.get("skip_autogen", False):
        return False

    return True


# ------------------------------------------------
# マイグレーションモード
# ------------------------------------------------
def run_migrations_offline() -> None:
    """
    オフラインモードでマイグレーションを実行
    DBに接続せず、実行すべきSQL文を標準出力へ書き出す
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # MATERIALIZED VIEW など無視する場合は下記をクラス属性に設定する
        # __table_args__ = {"info": {"skip_autogen": True}}
        include_object=include_object,
        # 型変更を検知する
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        dialect_opts={"paramstyle": "named"},
        # MATERIALIZED VIEW など無視する場合は下記をクラス属性に設定する
        # __table_args__ = {"info": {"skip_autogen": True}}
        include_object=include_object,
        # 型変更を検知する
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    非同期Engineを作成し、
    接続（Connection）を確立してAlembicのコンテキストに関連付ける。
    """

    connectable = async_engine

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    オンラインモードでマイグレーションを実行
    DB接続し、非同期で処理を行う
    """

    # 非同期関数を実行
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
