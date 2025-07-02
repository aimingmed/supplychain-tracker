from fastapi import APIRouter

from api.productlog.crud import (get_all_product_details,
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


@router.get("/product-inventory", response_model=list[ProductInventorySchema])
async def read_all_product_inventory():
    """
    Get all product inventory.
    """
    return await get_all_product_inventory()
