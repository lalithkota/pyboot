"""Module initializing configs"""

from pathlib import Path
from typing import Self

from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict

from .context import config_registry


class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="core_", env_file=".env", extra="allow", env_nested_delimiter="__"
    )

    logging_default_logger_name: str = "app"
    logging_level: str = "INFO"
    logging_file_name: Path | None = None

    @classmethod
    def get_config(cls, strict=True) -> Self:
        for config in config_registry:
            if isinstance(config, cls) and (not strict or type(config) is cls):
                return config
        new_config = cls()
        config_registry.append(new_config)
        return new_config
