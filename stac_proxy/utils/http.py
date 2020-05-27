from contextlib import asynccontextmanager

_aiohttp_session = None


class HttpClient:
    def __init__(self):
        self.session = _aiohttp_session

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
