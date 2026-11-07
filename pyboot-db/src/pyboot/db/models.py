"""Module containing base models"""

from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseORMModel(DeclarativeBase):
    __migrate_enabled__ = True
    __abstract__ = True
    __allow_unmapped__ = True
    __table_exists__: bool | None = None


class BaseORMModelWithId(BaseORMModel):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    active: Mapped[bool] = mapped_column()


class BaseORMModelWithTimes(BaseORMModelWithId):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(), default=lambda: datetime.now(tz=timezone.utc).replace(tzinfo=None)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(), default=lambda: datetime.now(tz=timezone.utc).replace(tzinfo=None)
    )
