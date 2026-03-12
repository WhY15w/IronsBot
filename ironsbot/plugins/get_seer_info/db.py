from collections.abc import Generator

import seerapi_models as seerapi_models
from nonebot import get_driver
from sqlalchemy.engine.base import Engine
from sqlmodel import Session as SQLModelSession
from sqlmodel import SQLModel, create_engine

from .config import plugin_config

_driver = get_driver()
_engine: Engine


@_driver.on_startup
async def init_orm() -> None:
    global _engine
    _engine = create_engine(plugin_config.database_url)
    SQLModel.metadata.create_all(_engine)


def reload_engine() -> None:
    """重建数据库引擎，用于数据库文件被替换后刷新连接。

    旧引擎的连接池会被释放，但已检出的连接（正在使用的 session）不受影响。
    """
    global _engine
    try:
        old_engine = _engine
    except NameError:
        return
    _engine = create_engine(plugin_config.database_url)
    old_engine.dispose()


def get_session() -> Generator[SQLModelSession, None, None]:
    with SQLModelSession(_engine) as session:
        yield session
