from pydantic import BaseModel
from stac_pydantic import Extensions


class Landsat8VendorExtension(BaseModel):
    revision: str
    product_id: str
    scene_id: str
    column: int
    row: int
    tier: str
    processing_level: str

    class Config:
        allow_population_by_field_name = True
        alias_generator = lambda field_name: f"landsat:{field_name}"


Extensions.register("landsat", Landsat8VendorExtension)
