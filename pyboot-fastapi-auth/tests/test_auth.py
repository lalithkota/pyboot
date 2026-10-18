from pyboot.fastapi.app import Initializer
from pyboot.fastapi_auth.app import Initializer as AuthInitializer


def test_auth_initializer():
    Initializer()
    AuthInitializer()
