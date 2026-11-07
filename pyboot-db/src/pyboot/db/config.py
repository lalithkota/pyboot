"""Module initializing configs"""

from pydantic import model_validator

from pyboot.core.config import BaseSettings


class Settings(BaseSettings):
    db_dialect: str = "postgresql"
    db_username: str = ""
    db_password: str = ""
    db_hostname: str = "localhost"
    db_port: int = 5432
    db_dbname: str = ""
    db_logging: bool = False

    db_async_driver_enabled: bool = True
    db_sync_driver_enabled: bool = True
    db_async_driver: str = "asyncpg"
    db_sync_driver: str = "psycopg"

    # If empty, these datasource configs will be constructed like this
    # f"{db_driver}://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_dbname}"
    db_sync_datasource: str = ""
    db_async_datasource: str = ""

    @model_validator(mode="after")
    def validate_db_datasource(self):
        if not self.db_sync_datasource:
            datasource = ""
            if self.db_dialect:
                datasource += f"{self.db_dialect}"
            if self.db_sync_driver:
                datasource += f"+{self.db_sync_driver}"
            datasource += "://"
            if self.db_username:
                datasource += f"{self.db_username}:{self.db_password}@"
            if self.db_hostname:
                datasource += self.db_hostname
            if self.db_port:
                datasource += f":{self.db_port}"
            if self.db_dbname:
                datasource += f"/{self.db_dbname}"

            self.db_sync_datasource = datasource
        if not self.db_async_datasource:
            datasource = ""
            if self.db_dialect:
                datasource += f"{self.db_dialect}"
            if self.db_async_driver:
                datasource += f"+{self.db_async_driver}"
            datasource += "://"
            if self.db_username:
                datasource += f"{self.db_username}:{self.db_password}@"
            if self.db_hostname:
                datasource += self.db_hostname
            if self.db_port:
                datasource += f":{self.db_port}"
            if self.db_dbname:
                datasource += f"/{self.db_dbname}"

            self.db_async_datasource = datasource
        return self
