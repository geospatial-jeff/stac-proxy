from typing import List, Optional

import aiohttp
from fastapi import FastAPI

import logging

logger = logging.getLogger(__name__)

from . import datasources

DEFAULT_INCLUDES = {"Landsat8"}


def create_app(
    includes: Optional[List[str]] = None, excludes: Optional[List[str]] = None
) -> FastAPI:
    includes = DEFAULT_INCLUDES if not includes else set(includes)
    excludes = set() if not excludes else set(excludes)

    app = FastAPI()

    async def _startup():
        session = aiohttp.ClientSession()
        for datasource in includes - excludes:
            ds = getattr(datasources, datasource)(session)
            app.include_router(ds._create_router())

    app.add_event_handler("startup", _startup)

    return app
