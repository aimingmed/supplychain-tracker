from typing import List
from fastapi import APIRouter, Depends, HTTPException

from api.productlog.crud import (create_product_details,
                                 get_all_product_details,
                                 get_all_product_inventory,
                                 get_product_inventory_by_product_id,
                                 update_product_details,
                                 get_product_details_by_id,
                                 delete_product_details,
                                 create_product_inventory,
                                 get_product_inventory_by_id,
                                 update_product_inventory,
                                 delete_product_inventory)
from models.productlog.pydantic import (ProductDetailsSchema,
                                        ProductInventorySchema,
                                        ProductInventoryCreateSchema,
                                        ProductInventoryWithDetailsSchema)
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


@router.get("/product-inventory", response_model=List[ProductInventoryWithDetailsSchema])
async def read_all_product_inventory():
    """
    Get all product inventory with complete product details.
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


# ProductInventory endpoints
@router.post("/product-inventory", response_model=ProductInventorySchema)
async def create_product_inventory_endpoint(
    data: ProductInventoryCreateSchema, 
    auth_details=Depends(auth_handler.auth_wrapper)
):
    """
    Create a new product inventory record.
    
    Args:
        data (ProductInventoryCreateSchema): The product inventory to create.
        auth_details (dict, optional): Authentication details containing user roles and username. 
            Defaults to Depends(auth_handler.auth_wrapper).
    
    Raises:
        HTTPException: If the user does not have permission to create inventory.
        HTTPException: If there's an error creating the inventory.
    
    Returns:
        ProductInventorySchema: The created product inventory.
    """
    list_of_roles = auth_details["list_of_roles"]
    
    # Check if user has ADMIN, PRODUCTION_MANAGER, or PRODUCER role
    if "ADMIN" not in list_of_roles and "PRODUCTION_MANAGER" not in list_of_roles and "PRODUCER" not in list_of_roles:
        raise HTTPException(
            status_code=403, 
            detail="You do not have permission to create inventory. Only ADMIN, PRODUCTION_MANAGER, or PRODUCER roles are allowed."
        )
    
    try:
        return await create_product_inventory(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/product-inventory/by-product/{product_id}", response_model=List[ProductInventorySchema])
async def get_product_inventory_by_product_endpoint(product_id: str):
    """
    Get all product inventory records for a specific product ID.
    
    Args:
        product_id (str): The product ID to get inventory for.
    
    Raises:
        HTTPException: If the product is not found.
    
    Returns:
        List[ProductInventorySchema]: List of product inventory records.
    """
    try:
        return await get_product_inventory_by_product_id(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/product-inventory/{batch_id}", response_model=ProductInventorySchema)
async def get_product_inventory_endpoint(batch_id: str):
    """
    Get a single product inventory record by batch ID.
    
    Args:
        batch_id (str): The internal batch ID of the inventory to retrieve.
    
    Raises:
        HTTPException: If the inventory is not found.
    
    Returns:
        ProductInventorySchema: The product inventory.
    """
    try:
        return await get_product_inventory_by_id(batch_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/product-inventory/{batch_id}", response_model=ProductInventorySchema)
async def update_product_inventory_endpoint(
    batch_id: str,
    data: ProductInventoryCreateSchema, 
    auth_details=Depends(auth_handler.auth_wrapper)
):
    """
    Update an existing product inventory record.
    
    Args:
        batch_id (str): The internal batch ID of the inventory to update.
        data (ProductInventoryCreateSchema): The updated product inventory.
        auth_details (dict, optional): Authentication details containing user roles and username. 
            Defaults to Depends(auth_handler.auth_wrapper).
    
    Raises:
        HTTPException: If the user does not have permission to update inventory.
        HTTPException: If the inventory is not found.
        HTTPException: If there's an error updating the inventory.
    
    Returns:
        ProductInventorySchema: The updated product inventory.
    """
    list_of_roles = auth_details["list_of_roles"]
    
    # Check if user has ADMIN, PRODUCTION_MANAGER, or PRODUCER role
    if "ADMIN" not in list_of_roles and "PRODUCTION_MANAGER" not in list_of_roles and "PRODUCER" not in list_of_roles:
        raise HTTPException(
            status_code=403, 
            detail="You do not have permission to update inventory. Only ADMIN, PRODUCTION_MANAGER, or PRODUCER roles are allowed."
        )
    
    try:
        return await update_product_inventory(batch_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/product-inventory/{batch_id}")
async def delete_product_inventory_endpoint(
    batch_id: str,
    auth_details=Depends(auth_handler.auth_wrapper)
):
    """
    Delete an existing product inventory record.
    
    Args:
        batch_id (str): The internal batch ID of the inventory to delete.
        auth_details (dict, optional): Authentication details containing user roles and username. 
            Defaults to Depends(auth_handler.auth_wrapper).
    
    Raises:
        HTTPException: If the user does not have permission to delete inventory.
        HTTPException: If the inventory is not found.
        HTTPException: If there's an error deleting the inventory.
    
    Returns:
        dict: Success message with deleted batch ID.
    """
    list_of_roles = auth_details["list_of_roles"]
    
    # Check if user has ADMIN, PRODUCTION_MANAGER, or PRODUCER role
    if "ADMIN" not in list_of_roles and "PRODUCTION_MANAGER" not in list_of_roles and "PRODUCER" not in list_of_roles:
        raise HTTPException(
            status_code=403, 
            detail="You do not have permission to delete inventory. Only ADMIN, PRODUCTION_MANAGER, or PRODUCER roles are allowed."
        )
    
    try:
        return await delete_product_inventory(batch_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
