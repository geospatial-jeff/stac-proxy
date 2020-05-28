from contextlib import asynccontextmanager
from dataclasses import dataclass

import aiohttp

@dataclass
class HttpClient:
    session: aiohttp.ClientSession

    @asynccontextmanager
    async def get(self, url, *args, **kwargs):
        async with self.session.get(url, *args, **kwargs) as resp:
            resp.raise_for_status()
            yield resp

    @asynccontextmanager
    async def post(self, url, *args, **kwargs):
        async with self.session.post(url, *args, **kwargs) as resp:
            resp.raise_for_status()
            yield resp
