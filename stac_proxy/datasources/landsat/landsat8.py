from dataclasses import dataclass
from typing import ClassVar
from urllib.parse import urljoin

from stac_pydantic import Collection, Item, ItemCollection
from stac_pydantic.collection import Extent, SpatialExtent, TimeInterval

from stac_proxy.datasources.base import Datasource
from stac_proxy.utils.http import HttpClient


@dataclass
class Landsat8(HttpClient, Datasource):
    base_url: ClassVar[str] = "https://earth-search.aws.element84.com"

    def _update_item(self, item):
        item["collection"] = item["properties"].pop("collection")
        item["stac_version"] = "0.9.0"
        item['stac_extensions'] = ["eo", "landsat", "proj", "view"]
        # STAC common metadata
        item['properties']['platform'] = item['properties'].pop('eo:platform')
        item['properties']['instruments'] = [item['properties'].pop('eo:instrument')]
        # Proj extension
        item['properties']['proj:epsg'] = item['properties'].pop('eo:epsg')
        item['properties']['landsat:column'] = item['properties'].pop('eo:column')
        item['properties']['landsat:row'] = item['properties'].pop('eo:row')
        # View extension
        item['properties']['view:off_nadir'] = item['properties'].pop('eo:off_nadir')
        item['properties']['view:sun_azimuth'] = item['properties'].pop('eo:sun_azimuth')
        item['properties']['view:sun_elevation'] = item['properties'].pop('eo:sun_elevation')
        return item

    async def collection(self) -> Collection:
        async with self.get(
            urljoin(self.base_url, f"/collections/landsat-8-l1")
        ) as resp:
            resp_json = await resp.json()
            resp_json['stac_version'] = "0.9.0"
            resp_json['extent'] = Extent(
                spatial=SpatialExtent(
                    bbox=[resp_json['extent']['spatial']]
                ),
                temporal=TimeInterval(
                    interval=[resp_json['extent']['temporal']]
                )
            )
        return Collection.parse_obj(resp_json)

    async def item(self, itemId) -> Item:
        async with self.get(
            urljoin(self.base_url, f"/collections/landsat-8-l1/items/{itemId}")
        ) as resp:
            resp_json = await resp.json()

        return Item.parse_obj(self._update_item(resp_json))

    async def search(self) -> ItemCollection:
        query_body = {"query": {"collection": {"eq": "landsat-8-l1"}}}

        async with self.post(
            urljoin(self.base_url, "/stac/search"), json=query_body
        ) as resp:
            resp_json = await resp.json()

        for item in resp_json["features"]:
            self._update_item(item)

        return ItemCollection.parse_obj(resp_json)
