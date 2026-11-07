"""Module for initializing Contexts"""

from fastapi import FastAPI

app_registry: FastAPI | None = None
