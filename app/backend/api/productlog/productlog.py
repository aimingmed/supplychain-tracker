from fastapi import APIRouter, HTTPException

from api.productlog.crud import (create_product_details,
                                 get_all_product_details,
                                 get_all_product_inventory)
from models.productlog.pydantic import (ProductDetailsSchema,
                                        ProductInventorySchema)

router = APIRouter()


@router.get("/product-details", response_model=list[ProductDetailsSchema])
async def read_all_product_details():
    """
    Get all product details.
    """
    return await get_all_product_details()


@router.post("/product-details", response_model=ProductDetailsSchema)
async def create_product_details_endpoint(data: ProductDetailsSchema):
    """
    Create a new product details record.
    """
    try:
        return await create_product_details(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/product-inventory", response_model=list[ProductInventorySchema])
async def read_all_product_inventory():
    """
    Get all product inventory.
    """
    return await get_all_product_inventory()
