"""Module initializing configs"""

from pathlib import Path
from typing import Self

from pydantic_settings import BaseSettings, SettingsConfigDict

from .context import config_registry


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="core_", env_file=".env", extra="allow", env_nested_delimiter="__"
    )

    logging_default_logger_name: str = "app"
    logging_level: str = "INFO"
    logging_file_name: Path | None = None

    error_response_debug: bool = False

    @classmethod
    def get_config(cls, strict=True) -> Self:
        result = None
        cr = config_registry.get()
        if not cr:
            cr = []
            config_registry.set(cr)
        for config in cr:
            if strict:
                if cls is type(config):
                    result = config
                    break
            else:
                if isinstance(config, cls):
                    result = config
                    break
        if not result:
            result = cls()
            cr.append(result)
        return result
