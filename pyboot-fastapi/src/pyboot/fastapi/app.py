"""Module containing initialization instructions and FastAPI app"""

from .config import Settings, WorkerType

_config = Settings.get_config(strict=False)

import logging
from contextlib import asynccontextmanager

import json_logging
import orjson
import uvicorn
from fastapi import FastAPI

from pyboot.core.app import BaseInitializer
from pyboot.core.context import component_registry
from pyboot.core.service import BaseAsyncService, BaseService

from . import context
from .exception import BaseExceptionHandler

_logger = logging.getLogger(_config.logging_default_logger_name)


class Initializer(BaseInitializer):
    def initialize_components(self):
        super().initialize_components()
        self.init_fastapi()

    def init_logger(self):
        logger = super().init_logger()
        json_logging.JSON_SERIALIZER = lambda log: orjson.dumps(log).decode("utf-8")
        json_logging.init_fastapi(enable_json=True)
        return logger

    def main_create_parser(self):
        parser, sp = super().main_create_parser()
        run_subparser = sp.add_parser("run", help="Run API Server.")
        run_subparser.set_defaults(func=self.fastapi_run_server)
        openapi_subparser = sp.add_parser("getOpenAPI", help="Get OpenAPI Json of the Server.")
        openapi_subparser.add_argument("filepath", help="Path of the Output OpenAPI Json File.")
        openapi_subparser.set_defaults(func=self.fastapi_get_openapi)
        return parser, sp

    def init_fastapi(self):
        app = FastAPI(
            title=_config.openapi_title,
            version=_config.openapi_version,
            description=_config.openapi_description,
            contact={
                "url": _config.openapi_contact_url,
                "email": _config.openapi_contact_email,
            },
            license_info={
                "name": _config.openapi_license_name,
                "url": _config.openapi_license_url,
            },
            lifespan=self.fastapi_app_lifespan,
            root_path=_config.openapi_root_path if _config.openapi_root_path else "",
        )
        json_logging.init_request_instrument(app)
        context.app_registry = app
        self.fastapi_create_exception_handler()
        _logger.info(
            "Worker ID - %s. Docker Pod ID - %s",
            _config.worker_id,
            _config.docker_pod_id,
        )

    def fastapi_create_exception_handler(self):
        return BaseExceptionHandler()

    def fastapi_return_app(self):
        return context.app_registry

    def fastapi_run_server(self, args):
        if _config.worker_type == WorkerType.gunicorn:
            import subprocess

            subprocess.run(
                f'gunicorn "main:app" --workers {_config.no_of_workers} --worker-class uvicorn.workers.UvicornWorker --bind {_config.host}:{_config.port}',
                check=False,
                shell=True,
            )
        if _config.worker_type == WorkerType.uvicorn:
            import subprocess

            subprocess.run(
                f'uvicorn "main:app" --workers {_config.no_of_workers} --host {_config.host} --port {_config.port}',
                check=False,
                shell=True,
            )
        if _config.worker_type == WorkerType.local:
            app = self.fastapi_return_app()
            if app is None:
                return
            uvicorn.run(
                app,
                host=_config.host,
                port=_config.port,
                access_log=False,
                # The following is not possible
                # workers=_config.no_of_workers
            )

    def fastapi_get_openapi(self, args):
        app = self.fastapi_return_app()
        if app is None:
            return
        with open(args.filepath, "wb+") as f:
            f.write(orjson.dumps(app.openapi(), option=orjson.OPT_INDENT_2))
            f.write(b"\n")

    async def fastapi_app_startup(self, app: FastAPI):
        """
        Override this method to execute something on startup
        """

    async def fastapi_app_shutdown(self, app: FastAPI):
        """
        Override this method to execute something on shutdown
        """

    @asynccontextmanager
    async def fastapi_app_lifespan(self, app: FastAPI):
        for component in component_registry:
            if isinstance(component, Initializer):
                await component.fastapi_app_startup(app)
        yield
        for component in component_registry:
            if isinstance(component, Initializer):
                await component.fastapi_app_shutdown(app)
            elif isinstance(component, BaseService):
                component.close()
            elif isinstance(component, BaseAsyncService):
                await component.aclose()
