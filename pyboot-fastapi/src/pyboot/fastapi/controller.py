"""Module from initializing base controllers"""

from fastapi.routing import APIRouter

from pyboot.core.component import BaseComponent

from .config import Settings
from .context import app_registry
from .errors import ErrorListResponse

_config = Settings.get_config(strict=False)


class BaseController(BaseComponent):
    def __init__(self, name="", **kwargs):
        super().__init__(name=name, **kwargs)
        self.router = APIRouter(
            responses={
                401: {"model": ErrorListResponse},
                403: {"model": ErrorListResponse},
                404: {"model": ErrorListResponse},
                500: {"model": ErrorListResponse},
            },
            **kwargs,
        )
        if _config.openapi_common_api_prefix:
            self.router.prefix = _config.openapi_common_api_prefix

    def post_init(self):
        # This is method is seperate from init, to allow overriding of __init__
        # while keeping post_init behaviour same for all subclasses.
        if app_registry:
            app_registry.include_router(self.router)
        return self
