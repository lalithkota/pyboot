"""Module for initializing Contexts"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .component import BaseComponent
    from .config import BaseSettings

config_registry: list["BaseSettings"] = []
component_registry: list["BaseComponent"] = []
