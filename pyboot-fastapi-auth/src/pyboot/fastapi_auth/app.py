"""Module initializing auth for APIs"""

from .config import Settings

_config = Settings.get_config(strict=False)

from pyboot.fastapi.app import Initializer as BaseInitializer

from .controllers.auth_controller import AuthController
from .controllers.oauth_controller import OAuthController


class Initializer(BaseInitializer):
    def initialize_components(self):
        super().initialize_components()
        AuthController().post_init()
        OAuthController().post_init()
