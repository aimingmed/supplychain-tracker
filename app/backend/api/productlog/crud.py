from models.productlog.pydantic import \
    ProductDetailsSchema as ProductDetailsCreateSchema
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
