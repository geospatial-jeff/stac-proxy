from dataclasses import dataclass
from typing import ClassVar
from urllib.parse import urljoin

from fastapi import Depends

from .base import Datasource
from ..utils.http import HttpClient


@dataclass
class Landsat8(Datasource):
    base_url: ClassVar[str] = "https://earth-search.aws.element84.com"

    async def item(self, itemId, http_client: HttpClient = Depends(HttpClient)):
        async with http_client.get(
            urljoin(self.base_url, f"/collections/landsat-8-l1/items/{itemId}")
        ) as resp:
            resp_json = await resp.json()
            resp_json["collection"] = resp_json["properties"].pop("collection")
            resp_json["stac_version"] = "0.9.0"

        return resp_json

    async def search(self, http_client: HttpClient = Depends(HttpClient)):
        query_body = {"query": {"collection": {"eq": "landsat-8-l1"}}}

        async with http_client.post(
            urljoin(self.base_url, "/stac/search"), json=query_body
        ) as resp:
            resp_json = await resp.json()

        for item in resp_json["features"]:
            item["collection"] = item["properties"].pop("collection")
            item["stac_version"] = "0.9.0"

        return resp_json
