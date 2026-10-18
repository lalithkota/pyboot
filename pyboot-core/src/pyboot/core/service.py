"""Module for initiailizing base Service"""

from .component import BaseComponent


class BaseSyncService(BaseComponent):
    def __init__(self, name=""):
        super().__init__(name)

    def close(self):
        """To be implemented by submodule."""


class BaseAsyncService(BaseComponent):
    def __init__(self, name=""):
        super().__init__(name)

    async def aclose(self):
        """To be implemented by submodule."""
