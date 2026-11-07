"""Module containing initialization instructions and FastAPI app"""

import logging

from pyboot.core.app import BaseInitializer

from .config import Settings
from .service import BaseDbAsyncService, BaseDbService

_config = Settings.get_config(strict=False)
_logger = logging.getLogger(_config.logging_default_logger_name)


class Initializer(BaseInitializer):
    def initialize_components(self):
        super().initialize_components()
        self.init_db()

    def main_create_parser(self):
        parser, sp = super().main_create_parser()
        migrate_subparser = sp.add_parser("migrate", help="Create/Migrate Database Tables.")
        migrate_subparser.set_defaults(func=self.migrate_database)
        return parser, sp

    def init_db(self):
        """
        Initialize Database components. Override this method in custom Initializer impl
        if you don't want to use BaseDbAsyncService & BaseDbService.
        """
        if _config.db_sync_driver_enabled:
            BaseDbService()
        if _config.db_async_driver_enabled:
            BaseDbAsyncService()

    def migrate_database(self, args):
        """
        Implement the logic for the 'migrate' subcommand here.
        For example subclasses can override this method like:
        ```python
        def migrate_database(self, args):
            super().migrate_database(args)
            db_service = BaseDbService.get_component()
            db_service.create_migrate(MyOrmModel)
            db_service.create_migrate(NewOrmModel)
        ```
        Or use async service like:
        ```python
        def migrate_database(self, args):
            super().migrate_database(args)
            db_service = BaseDbAsyncService.get_component()
            async def migrate():
                await db_service.create_migrate(MyOrmModel)
                await db_service.create_migrate(NewOrmModel)
            asyncio.run(migrate())
        ```
        """
        _logger.info("Starting DB migrations.")
