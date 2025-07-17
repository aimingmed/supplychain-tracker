from typing import List
from fastapi import APIRouter, Depends, HTTPException

from api.productlog.crud import (create_product_details,
                                 get_all_product_details,
                                 get_all_product_inventory,
                                 update_product_details,
                                 get_product_details_by_id,
                                 delete_product_details)
from models.productlog.pydantic import (ProductDetailsSchema,
                                        ProductInventorySchema)
from models.requests.authentication import AuthHandler

router = APIRouter()
auth_handler = AuthHandler()


@router.get("/product-details", response_model=List[ProductDetailsSchema])
async def read_all_product_details():
    """
    Get all product details.
    """
    return await get_all_product_details()


@router.post("/product-details", response_model=ProductDetailsSchema)
async def create_product_details_endpoint(
    data: ProductDetailsSchema, auth_details=Depends(auth_handler.auth_wrapper)
):
    """
    Create a new product details record.
    
    Args:
        data (ProductDetailsSchema): The product details to create.
        auth_details (dict, optional): Authentication details containing user roles and username. 
            Defaults to Depends(auth_handler.auth_wrapper).
    
    Raises:
        HTTPException: If the user does not have permission to create products.
        HTTPException: If there's an error creating the product.
    
    Returns:
        ProductDetailsSchema: The created product details.
    """
    list_of_roles = auth_details["list_of_roles"]
    
    # Check if user has ADMIN or PRODUCTION_MANAGER role
    if "ADMIN" not in list_of_roles and "PRODUCTION_MANAGER" not in list_of_roles:
        raise HTTPException(
            status_code=403, 
            detail="You do not have permission to create products. Only ADMIN or PRODUCTION_MANAGER roles are allowed."
        )
    
    try:
        return await create_product_details(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/product-inventory", response_model=List[ProductInventorySchema])
async def read_all_product_inventory():
    """
    Get all product inventory.
    """
    return await get_all_product_inventory()


@router.get("/product-details/{product_id}", response_model=ProductDetailsSchema)
async def get_product_details_endpoint(product_id: str):
    """
    Get a single product details record by product ID.
    
    Args:
        product_id (str): The ID of the product to retrieve.
    
    Raises:
        HTTPException: If the product is not found.
    
    Returns:
        ProductDetailsSchema: The product details.
    """
    try:
        return await get_product_details_by_id(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/product-details/{product_id}", response_model=ProductDetailsSchema)
async def update_product_details_endpoint(
    product_id: str,
    data: ProductDetailsSchema, 
    auth_details=Depends(auth_handler.auth_wrapper)
):
    """
    Update an existing product details record.
    
    Args:
        product_id (str): The ID of the product to update.
        data (ProductDetailsSchema): The updated product details.
        auth_details (dict, optional): Authentication details containing user roles and username. 
            Defaults to Depends(auth_handler.auth_wrapper).
    
    Raises:
        HTTPException: If the user does not have permission to update products.
        HTTPException: If the product is not found.
        HTTPException: If there's an error updating the product.
    
    Returns:
        ProductDetailsSchema: The updated product details.
    """
    list_of_roles = auth_details["list_of_roles"]
    
    # Check if user has ADMIN or PRODUCTION_MANAGER role
    if "ADMIN" not in list_of_roles and "PRODUCTION_MANAGER" not in list_of_roles:
        raise HTTPException(
            status_code=403, 
            detail="You do not have permission to update products. Only ADMIN or PRODUCTION_MANAGER roles are allowed."
        )
    
    try:
        return await update_product_details(product_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/product-details/{product_id}")
async def delete_product_details_endpoint(
    product_id: str,
    auth_details=Depends(auth_handler.auth_wrapper)
):
    """
    Delete an existing product details record.
    
    Args:
        product_id (str): The ID of the product to delete.
        auth_details (dict, optional): Authentication details containing user roles and username. 
            Defaults to Depends(auth_handler.auth_wrapper).
    
    Raises:
        HTTPException: If the user does not have permission to delete products.
        HTTPException: If the product is not found.
        HTTPException: If there's an error deleting the product.
    
    Returns:
        dict: Success message with deleted product ID.
    """
    list_of_roles = auth_details["list_of_roles"]
    
    # Check if user has ADMIN or PRODUCTION_MANAGER role
    if "ADMIN" not in list_of_roles and "PRODUCTION_MANAGER" not in list_of_roles:
        raise HTTPException(
            status_code=403, 
            detail="You do not have permission to delete products. Only ADMIN or PRODUCTION_MANAGER roles are allowed."
        )
    
    try:
        return await delete_product_details(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
