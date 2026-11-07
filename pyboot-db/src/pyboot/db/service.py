"""Module containing base models"""

import logging
from typing import TypeVar

from sqlalchemy import create_engine, inspect, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from pyboot.core.service import BaseAsyncService, BaseService

from .config import Settings
from .models import BaseORMModel, BaseORMModelWithId

_config = Settings.get_config(strict=False)
_logger = logging.getLogger(_config.logging_default_logger_name)

_BaseOrmModelWithId_TypeVar = TypeVar("_BaseOrmModelWithId_TypeVar", bound=BaseORMModelWithId)


class BaseDbService(BaseService):
    def __init__(self, name="", **kw):
        super().__init__(name=name, **kw)
        self.dbengine = create_engine(_config.db_sync_datasource, echo=_config.db_logging)
        self.session_maker = sessionmaker(bind=self.dbengine)

    def close(self):
        """Closes this Db service instance. This closes any existing connections and closes the engine."""
        self.dbengine.dispose()
        del self.dbengine

    def get_engine(self):
        return self.dbengine

    def create_migrate(self, orm_model: type[BaseORMModel]):
        if not orm_model.__migrate_enabled__:
            return
        orm_model.metadata.create_all(
            self.get_engine(),
            # To ensure only selected table is created
            # without creating relationship tables.
            tables=[orm_model.__table__],
        )

    def table_exists_cached(self, orm_model: type[BaseORMModel]) -> bool:
        if orm_model.__abstract__:
            return False
        if orm_model.__table_exists__ is not None:
            return orm_model.__table_exists__
        orm_model.__table_exists__ = inspect(self.get_engine()).has_table(orm_model.__tablename__)
        return orm_model.__table_exists__

    def update_to_db(self, *objs: BaseORMModel):
        with self.session_maker() as session:
            for obj in objs:
                session.merge(obj)
            session.commit()

    def get_obj_by_id(
        self, orm_model: type[_BaseOrmModelWithId_TypeVar], id: int, active=True
    ) -> _BaseOrmModelWithId_TypeVar | None:
        result = None
        with self.session_maker() as session:
            result = session.get(orm_model, id)
            if (not result) or (result.active != active):
                result = None

        return result

    def get_all_objs(
        self, orm_model: type[_BaseOrmModelWithId_TypeVar], active=True
    ) -> list[_BaseOrmModelWithId_TypeVar]:
        response = []
        with self.session_maker() as session:
            stmt = select(orm_model).where(orm_model.active == active).order_by(orm_model.id.asc())

            result = session.execute(stmt)

            response = list(result.scalars())
        return response


class BaseDbAsyncService(BaseAsyncService):
    def __init__(self, name="", **kw):
        super().__init__(name=name, **kw)
        self.dbengine = create_async_engine(_config.db_async_datasource, echo=_config.db_logging)
        self.session_maker = async_sessionmaker(bind=self.dbengine)

    async def aclose(self):
        """Closes this Db service instance. This closes any existing connections and closes the engine."""
        await self.dbengine.dispose()
        del self.dbengine

    def get_engine(self):
        return self.dbengine

    async def create_migrate(self, orm_model: type[BaseORMModel]):
        if not orm_model.__migrate_enabled__:
            return
        async with self.get_engine().begin() as conn:
            await conn.run_sync(
                lambda sconn: orm_model.metadata.create_all(
                    sconn,
                    # To ensure only selected table is created
                    # without creating relationship tables.
                    tables=[orm_model.__table__],
                )
            )

    async def table_exists_cached(self, orm_model: type[BaseORMModel]) -> bool:
        if orm_model.__abstract__:
            return False
        if orm_model.__table_exists__ is not None:
            return orm_model.__table_exists__
        async with self.get_engine().begin() as conn:
            orm_model.__table_exists__ = await conn.run_sync(
                lambda sconn: inspect(sconn).has_table(orm_model.__tablename__)
            )
            return orm_model.__table_exists__

    async def update_to_db(self, *objs: BaseORMModel):
        async with self.session_maker() as session:
            for obj in objs:
                await session.merge(obj)
            await session.commit()

    async def get_obj_by_id(
        self, orm_model: type[_BaseOrmModelWithId_TypeVar], id: int, active=True
    ) -> _BaseOrmModelWithId_TypeVar | None:
        result = None
        async with self.session_maker() as session:
            result = await session.get(orm_model, id)
            if (not result) or (result.active != active):
                result = None

        return result

    async def get_all_objs(
        self, orm_model: type[_BaseOrmModelWithId_TypeVar], active=True
    ) -> list[_BaseOrmModelWithId_TypeVar]:
        response = []
        async with self.session_maker() as session:
            stmt = select(orm_model).where(orm_model.active == active).order_by(orm_model.id.asc())

            result = await session.execute(stmt)

            response = list(result.scalars())
        return response
