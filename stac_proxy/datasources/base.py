import abc

from dataclasses import dataclass
from fastapi import APIRouter
from stac_pydantic import Collection, ItemCollection, Item


@dataclass
class Datasource(abc.ABC):
    @abc.abstractmethod
    async def search(self) -> ItemCollection:
        ...

    @abc.abstractmethod
    async def collection(self) -> Collection:
        ...

    @abc.abstractmethod
    async def item(self, item_id) -> Item:
        ...

    def _create_router(self) -> APIRouter:
        router = APIRouter()
        router.add_api_route(
            path=f"/{self.__class__.__name__.lower()}/search",
            endpoint=self.search,
            methods=["POST", "GET"],
            response_model=ItemCollection,
            response_model_exclude_unset=True,
        )
        router.add_api_route(
            path=f"/collections/{self.__class__.__name__.lower()}/items/{{itemId}}",
            endpoint=self.item,
            methods=["GET"],
            response_model=Item,
            response_model_exclude_unset=True,
        )
        router.add_api_route(
            path=f"/collections/{self.__class__.__name__.lower()}",
            endpoint=self.collection,
            methods=["GET"],
            response_model=Collection,
            response_model_exclude_unset=True
        )
        return router
