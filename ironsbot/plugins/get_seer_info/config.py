from pathlib import Path

from nonebot import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    seerapi_sync_url: str = ""
    seerapi_sync_interval_minutes: int = 60
    seerapi_local_path: str = "seerapi-data.sqlite"
    alias_sync_url: str = ""
    alias_sync_interval_minutes: int = 60
    alias_local_path: str = "aliases-data.sqlite"
    render_cache_dir: Path | None = None
    render_cache_max_size_mb: int = 200


plugin_config = get_plugin_config(Config)
