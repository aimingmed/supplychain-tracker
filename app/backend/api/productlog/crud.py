from models.productlog.tortoise import (ProductDetails, ProductDetailsSchema,
                                        ProductInventory,
                                        ProductInventorySchema)


async def get_all_product_details():
    """
    Fetch all product details from the database and return as a list of ProductDetailsSchema.
    """
    return await ProductDetailsSchema.from_queryset(ProductDetails.all())


async def get_all_product_inventory():
    """
    Fetch all product inventory from the database and return as a list of ProductInventorySchema.
    """
    return await ProductInventorySchema.from_queryset(ProductInventory.all())
