from typing import List, Optional

import aiohttp
from fastapi import FastAPI


from . import datasources
from .utils import http


DEFAULT_INCLUDES = {"Landsat8"}


async def _startup():
    http._aiohttp_session = aiohttp.ClientSession()


async def _shutdown():
    await http._aiohttp_session.close()


def create_app(
    includes: Optional[List[str]] = None, excludes: Optional[List[str]] = None
) -> FastAPI:
    includes = DEFAULT_INCLUDES if not includes else set(includes)
    excludes = set() if not excludes else set(excludes)
    app = FastAPI()
    for datasource in includes - excludes:
        ds = getattr(datasources, datasource)()
        app.include_router(ds._create_router())

    app.add_event_handler("startup", _startup)
    app.add_event_handler("shutdown", _shutdown)

    return app
