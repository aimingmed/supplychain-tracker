from typing import List, Optional
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, validator

class ProductStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    OUT_OF_STOCK = "OUT_OF_STOCK"

class ProductDetailsSchema(BaseModel):
    productid: str = Field(..., example="P12345")
    productname: str = Field(..., example="Product Name")
    categoryname: str = Field(..., example="Category Name")
    specification: str = Field(..., example="Specification")
    reorderlevel: int = Field(..., example=10)
    targetstocklevel: int = Field(..., example=100)
    leadtime: int = Field(..., example=5)

class ProductInventorySchema(ProductDetailsSchema):
    batchid: str = Field(..., example="B12345")
    quantityinstock: int = Field(..., example=50)
    productiondate: datetime = Field(..., example="2025-06-13")
    imageurl: Optional[str] = Field(None, example="http://example.com/image.jpg")
    status: ProductStatus = Field(..., example=ProductStatus.AVAILABLE)
    lastupdated: datetime = Field(default_factory=datetime.utcnow)
    lastupdatedby: str = Field(..., example="admin")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "productid": "P12345",
                "productname": "Product Name",
                "categoryname": "Category Name",
                "specification": "Specification",
                "reorderlevel": 10,
                "targetstocklevel": 100,
                "leadtime": 5,
                "batchid": "B12345",
                "quantityinstock": 50,
                "productiondate": "2025-06-13T00:00:00",
                "imageurl": "http://example.com/image.jpg",
                "status": ProductStatus.AVAILABLE,
                "lastupdated": "2025-06-13T12:00:00",
                "lastupdatedby": "admin"
            }
        }