from sqlalchemy import JSON, String
from sqlalchemy import Enum as SaEnum
from sqlalchemy.orm import Mapped, mapped_column

from pyboot.db.models import BaseORMModelWithTimes

from ...config import Settings
from ..login_provider import LoginProviderTypes

_config = Settings.get_config(strict=False)


class LoginProvider(BaseORMModelWithTimes):
    __migrate_enabled__ = _config.login_providers_table_enabled
    __tablename__ = _config.login_providers_table_name

    name: Mapped[str] = mapped_column(String())
    type: Mapped[LoginProviderTypes] = mapped_column(SaEnum(LoginProviderTypes))

    description: Mapped[str | None] = mapped_column(String())

    login_button_text: Mapped[str | None] = mapped_column(String())
    login_button_image_url: Mapped[str | None] = mapped_column(String())

    authorization_parameters: Mapped[dict | None] = mapped_column(JSON(), default={})
