from models.productlog.pydantic import \
    ProductDetailsSchema as ProductDetailsCreateSchema, \
    ProductInventoryCreateSchema
from models.productlog.tortoise import (ProductDetails, ProductDetailsSchema,
                                        ProductInventory,
                                        ProductInventorySchema)


async def get_all_product_details():
    """
    Fetch all product details from the database and return as a list of ProductDetailsSchema.
    """
    return await ProductDetailsSchema.from_queryset(ProductDetails.all())


async def create_product_details(data: ProductDetailsCreateSchema):
    """
    Create a new ProductDetails record in the database.
    """
    obj = await ProductDetails.create(**data.dict())
    return await ProductDetailsSchema.from_tortoise_orm(obj)


async def get_all_product_inventory():
    """
    Fetch all product inventory from the database and return as a list of ProductInventorySchema.
    """
    return await ProductInventorySchema.from_queryset(ProductInventory.all())


async def update_product_details(product_id: str, data: ProductDetailsCreateSchema):
    """
    Update an existing ProductDetails record in the database.
    """
    product = await ProductDetails.get_or_none(productid=product_id)
    if not product:
        raise ValueError(f"Product with ID {product_id} not found")
    
    # Update the product with new data
    await product.update_from_dict(data.dict(exclude_unset=True))
    await product.save()
    
    return await ProductDetailsSchema.from_tortoise_orm(product)


async def get_product_details_by_id(product_id: str):
    """
    Get a single product details record by product ID.
    """
    product = await ProductDetails.get_or_none(productid=product_id)
    if not product:
        raise ValueError(f"Product with ID {product_id} not found")
    
    return await ProductDetailsSchema.from_tortoise_orm(product)


async def delete_product_details(product_id: str):
    """
    Delete a ProductDetails record from the database.
    
    Args:
        product_id (str): The ID of the product to delete.
        
    Raises:
        ValueError: If the product is not found.
        
    Returns:
        dict: Success message with deleted product ID.
    """
    product = await ProductDetails.get_or_none(productid=product_id)
    if not product:
        raise ValueError(f"Product with ID {product_id} not found")
    
    await product.delete()
    return {"message": f"Product {product_id} deleted successfully", "product_id": product_id}


# ProductInventory CRUD operations
async def create_product_inventory(data: ProductInventoryCreateSchema):
    """
    Create a new ProductInventory record in the database.
    """
    # Exclude None values and auto-generated fields
    data_dict = data.dict(exclude_unset=True, exclude_none=True)
    # Remove auto-generated fields if they are present as None or empty
    data_dict.pop('batchid_internal', None)
    data_dict.pop('batchid_external', None)
    
    obj = await ProductInventory.create(**data_dict)
    return await ProductInventorySchema.from_tortoise_orm(obj)


async def get_product_inventory_by_id(batch_id: str):
    """
    Get a single product inventory record by batch ID.
    """
    inventory = await ProductInventory.get_or_none(batchid_internal=batch_id)
    if not inventory:
        raise ValueError(f"Product inventory with batch ID {batch_id} not found")
    
    return await ProductInventorySchema.from_tortoise_orm(inventory)


async def update_product_inventory(batch_id: str, data: ProductInventoryCreateSchema):
    """
    Update an existing ProductInventory record in the database.
    """
    inventory = await ProductInventory.get_or_none(batchid_internal=batch_id)
    if not inventory:
        raise ValueError(f"Product inventory with batch ID {batch_id} not found")
    
    # Update the inventory with new data, excluding auto-generated fields
    data_dict = data.dict(exclude_unset=True, exclude_none=True)
    # Remove auto-generated fields if they are present
    data_dict.pop('batchid_internal', None)
    data_dict.pop('batchid_external', None)
    
    await inventory.update_from_dict(data_dict)
    await inventory.save()
    
    return await ProductInventorySchema.from_tortoise_orm(inventory)


async def delete_product_inventory(batch_id: str):
    """
    Delete a ProductInventory record from the database.
    
    Args:
        batch_id (str): The internal batch ID of the inventory to delete.
        
    Raises:
        ValueError: If the inventory is not found.
        
    Returns:
        dict: Success message with deleted batch ID.
    """
    inventory = await ProductInventory.get_or_none(batchid_internal=batch_id)
    if not inventory:
        raise ValueError(f"Product inventory with batch ID {batch_id} not found")
    
    await inventory.delete()
    return {"message": f"Product inventory {batch_id} deleted successfully", "batch_id": batch_id}
