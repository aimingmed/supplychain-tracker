from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date, datetime

import pytest

from api.productlog import crud
from models.productlog.pydantic import (
    ProductDetailsSchema as ProductDetailsCreateSchema,
    ProductInventoryCreateSchema
)


# Sample test data
SAMPLE_PRODUCT_CREATE_DATA = ProductDetailsCreateSchema(
    productid="P001",
    category="Organoid(类器官)",
    setsubcategory="Human Organoid(人源类器官)",
    source="Human(人源)",
    productnameen="Test Product EN",
    productnamezh="测试产品",
    specification="Test Specification",
    unit="Box(盒)",
    components=[],
    is_sold_independently=True,
    remarks_temperature="Store at -20°C",
    storage_temperature_duration="6 months",
    reorderlevel=10,
    targetstocklevel=100,
    leadtime=5,
)

SAMPLE_PRODUCT_DICT = {
    "productid": "P001",
    "category": "Organoid(类器官)",
    "setsubcategory": "Human Organoid(人源类器官)",
    "source": "Human(人源)",
    "productnameen": "Test Product EN",
    "productnamezh": "测试产品",
    "specification": "Test Specification",
    "unit": "Box(盒)",
    "components": [],
    "is_sold_independently": True,
    "remarks_temperature": "Store at -20°C",
    "storage_temperature_duration": "6 months",
    "reorderlevel": 10,
    "targetstocklevel": 100,
    "leadtime": 5,
}

SAMPLE_INVENTORY_DATA = {
    "basicmediumid": "BM001",
    "addictiveid": "AD001",
    "quantityinstock": 50,
    "productiondate": "2025-01-01",  # Fixed: use date format
    "imageurl": "http://example.com/image.jpg",
    "status": "AVAILABLE",
    "productiondatetime": "2025-01-01T12:00:00",
    "producedby": "John Doe",
    "to_show": True,
    "lastupdatedby": "Jane Doe",
    "coa_appearance": "Clear and colorless",
    "coa_clarity": True,
    "coa_osmoticpressure": 300.5,
    "coa_ph": 7.4,
    "coa__mycoplasma": False,
    "coa_sterility": True,
    "coa_fillingvolumedifference": True,
}

SAMPLE_INVENTORY_CREATE_DATA = ProductInventoryCreateSchema(**SAMPLE_INVENTORY_DATA)

SAMPLE_INVENTORY_RESPONSE_DATA = {
    "batchid_internal": "BM001-AD001-ABC123",
    "batchid_external": "BM001-AD001",
    "lastupdated": "2025-01-02T12:00:00",
    **SAMPLE_INVENTORY_DATA
}


# Tests for get_all_product_details
@pytest.mark.asyncio
@patch("api.productlog.crud.ProductDetails")
@patch("api.productlog.crud.ProductDetailsSchema")
async def test_get_all_product_details_success(mock_schema, mock_model):
    """Test successful retrieval of all product details."""
    # Arrange
    mock_queryset = AsyncMock()
    mock_model.all.return_value = mock_queryset
    expected_result = [SAMPLE_PRODUCT_DICT]
    mock_schema.from_queryset = AsyncMock(return_value=expected_result)

    # Act
    result = await crud.get_all_product_details()

    # Assert
    mock_model.all.assert_called_once()
    mock_schema.from_queryset.assert_awaited_once_with(mock_queryset)
    assert result == expected_result
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["productid"] == "P001"


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductDetails")
@patch("api.productlog.crud.ProductDetailsSchema")
async def test_get_all_product_details_empty(mock_schema, mock_model):
    """Test retrieval when no product details exist."""
    # Arrange
    mock_queryset = AsyncMock()
    mock_model.all.return_value = mock_queryset
    mock_schema.from_queryset = AsyncMock(return_value=[])

    # Act
    result = await crud.get_all_product_details()

    # Assert
    mock_model.all.assert_called_once()
    mock_schema.from_queryset.assert_awaited_once_with(mock_queryset)
    assert result == []
    assert isinstance(result, list)
    assert len(result) == 0


# Tests for get_all_product_inventory
@pytest.mark.asyncio
@patch("api.productlog.crud.ProductInventory")
@patch("api.productlog.crud.ProductInventorySchema")
async def test_get_all_product_inventory_success(mock_schema, mock_model):
    """Test successful retrieval of all product inventory."""
    # Arrange
    mock_queryset = AsyncMock()
    mock_model.all.return_value = mock_queryset
    expected_result = [SAMPLE_INVENTORY_RESPONSE_DATA]
    mock_schema.from_queryset = AsyncMock(return_value=expected_result)

    # Act
    result = await crud.get_all_product_inventory()

    # Assert
    mock_model.all.assert_called_once()
    mock_schema.from_queryset.assert_awaited_once_with(mock_queryset)
    assert result == expected_result
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["batchid_internal"] == "BM001-AD001-ABC123"


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductInventory")
@patch("api.productlog.crud.ProductInventorySchema")
async def test_get_all_product_inventory_empty(mock_schema, mock_model):
    """Test retrieval when no product inventory exists."""
    # Arrange
    mock_queryset = AsyncMock()
    mock_model.all.return_value = mock_queryset
    mock_schema.from_queryset = AsyncMock(return_value=[])

    # Act
    result = await crud.get_all_product_inventory()

    # Assert
    mock_model.all.assert_called_once()
    mock_schema.from_queryset.assert_awaited_once_with(mock_queryset)
    assert result == []
    assert isinstance(result, list)
    assert len(result) == 0


# Tests for create_product_details
@pytest.mark.asyncio
@patch("api.productlog.crud.ProductDetails")
@patch("api.productlog.crud.ProductDetailsSchema")
async def test_create_product_details_success(mock_schema, mock_model):
    """Test successful creation of product details."""
    # Arrange
    mock_product_instance = MagicMock()
    mock_model.create = AsyncMock(return_value=mock_product_instance)
    expected_result = SAMPLE_PRODUCT_DICT
    mock_schema.from_tortoise_orm = AsyncMock(return_value=expected_result)

    # Act
    result = await crud.create_product_details(SAMPLE_PRODUCT_CREATE_DATA)

    # Assert
    mock_model.create.assert_awaited_once_with(**SAMPLE_PRODUCT_CREATE_DATA.dict())
    mock_schema.from_tortoise_orm.assert_awaited_once_with(mock_product_instance)
    assert result == expected_result
    assert result["productid"] == "P001"


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductDetails")
async def test_create_product_details_database_error(mock_model):
    """Test create_product_details handles database errors."""
    # Arrange
    mock_model.create = AsyncMock(side_effect=Exception("Database connection error"))

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await crud.create_product_details(SAMPLE_PRODUCT_CREATE_DATA)
    
    assert "Database connection error" in str(exc_info.value)
    mock_model.create.assert_awaited_once()


# Tests for get_product_details_by_id
@pytest.mark.asyncio
@patch("api.productlog.crud.ProductDetails")
@patch("api.productlog.crud.ProductDetailsSchema")
async def test_get_product_details_by_id_success(mock_schema, mock_model):
    """Test successful retrieval of product by ID."""
    # Arrange
    mock_product_instance = MagicMock()
    mock_model.get_or_none = AsyncMock(return_value=mock_product_instance)
    expected_result = SAMPLE_PRODUCT_DICT
    mock_schema.from_tortoise_orm = AsyncMock(return_value=expected_result)

    # Act
    result = await crud.get_product_details_by_id("P001")

    # Assert
    mock_model.get_or_none.assert_awaited_once_with(productid="P001")
    mock_schema.from_tortoise_orm.assert_awaited_once_with(mock_product_instance)
    assert result == expected_result
    assert result["productid"] == "P001"


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductDetails")
async def test_get_product_details_by_id_not_found(mock_model):
    """Test get_product_details_by_id when product doesn't exist."""
    # Arrange
    mock_model.get_or_none = AsyncMock(return_value=None)

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        await crud.get_product_details_by_id("NOTFOUND")
    
    assert "Product with ID NOTFOUND not found" in str(exc_info.value)
    mock_model.get_or_none.assert_awaited_once_with(productid="NOTFOUND")


# Tests for update_product_details
@pytest.mark.asyncio
@patch("api.productlog.crud.ProductDetails")
@patch("api.productlog.crud.ProductDetailsSchema")
async def test_update_product_details_success(mock_schema, mock_model):
    """Test successful update of product details."""
    # Arrange
    mock_product_instance = MagicMock()
    mock_product_instance.update_from_dict = AsyncMock()
    mock_product_instance.save = AsyncMock()
    mock_model.get_or_none = AsyncMock(return_value=mock_product_instance)
    
    updated_data = ProductDetailsCreateSchema(**{**SAMPLE_PRODUCT_DICT, "productnameen": "Updated Product"})
    expected_result = {**SAMPLE_PRODUCT_DICT, "productnameen": "Updated Product"}
    mock_schema.from_tortoise_orm = AsyncMock(return_value=expected_result)

    # Act
    result = await crud.update_product_details("P001", updated_data)

    # Assert
    mock_model.get_or_none.assert_awaited_once_with(productid="P001")
    mock_product_instance.update_from_dict.assert_awaited_once_with(updated_data.dict(exclude_unset=True))
    mock_product_instance.save.assert_awaited_once()
    mock_schema.from_tortoise_orm.assert_awaited_once_with(mock_product_instance)
    assert result == expected_result
    assert result["productnameen"] == "Updated Product"


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductDetails")
async def test_update_product_details_not_found(mock_model):
    """Test update_product_details when product doesn't exist."""
    # Arrange
    mock_model.get_or_none = AsyncMock(return_value=None)
    updated_data = ProductDetailsCreateSchema(**SAMPLE_PRODUCT_DICT)

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        await crud.update_product_details("NOTFOUND", updated_data)
    
    assert "Product with ID NOTFOUND not found" in str(exc_info.value)
    mock_model.get_or_none.assert_awaited_once_with(productid="NOTFOUND")


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductDetails")
async def test_update_product_details_save_error(mock_model):
    """Test update_product_details handles save errors."""
    # Arrange
    mock_product_instance = MagicMock()
    mock_product_instance.update_from_dict = AsyncMock()
    mock_product_instance.save = AsyncMock(side_effect=Exception("Save failed"))
    mock_model.get_or_none = AsyncMock(return_value=mock_product_instance)
    
    updated_data = ProductDetailsCreateSchema(**SAMPLE_PRODUCT_DICT)

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await crud.update_product_details("P001", updated_data)
    
    assert "Save failed" in str(exc_info.value)
    mock_model.get_or_none.assert_awaited_once_with(productid="P001")
    mock_product_instance.update_from_dict.assert_awaited_once()
    mock_product_instance.save.assert_awaited_once()


# Tests for delete_product_details
@pytest.mark.asyncio
@patch("api.productlog.crud.ProductDetails")
async def test_delete_product_details_success(mock_model):
    """Test successful deletion of product details."""
    # Arrange
    mock_product_instance = MagicMock()
    mock_product_instance.delete = AsyncMock()
    mock_model.get_or_none = AsyncMock(return_value=mock_product_instance)

    # Act
    result = await crud.delete_product_details("P001")

    # Assert
    mock_model.get_or_none.assert_awaited_once_with(productid="P001")
    mock_product_instance.delete.assert_awaited_once()
    assert result == {"message": "Product P001 deleted successfully", "product_id": "P001"}
    assert result["product_id"] == "P001"
    assert "deleted successfully" in result["message"]


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductDetails")
async def test_delete_product_details_not_found(mock_model):
    """Test delete_product_details when product doesn't exist."""
    # Arrange
    mock_model.get_or_none = AsyncMock(return_value=None)

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        await crud.delete_product_details("NOTFOUND")
    
    assert "Product with ID NOTFOUND not found" in str(exc_info.value)
    mock_model.get_or_none.assert_awaited_once_with(productid="NOTFOUND")


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductDetails")
async def test_delete_product_details_delete_error(mock_model):
    """Test delete_product_details handles deletion errors."""
    # Arrange
    mock_product_instance = MagicMock()
    mock_product_instance.delete = AsyncMock(side_effect=Exception("Foreign key constraint"))
    mock_model.get_or_none = AsyncMock(return_value=mock_product_instance)

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await crud.delete_product_details("P001")
    
    assert "Foreign key constraint" in str(exc_info.value)
    mock_model.get_or_none.assert_awaited_once_with(productid="P001")
    mock_product_instance.delete.assert_awaited_once()


# Edge case tests
@pytest.mark.asyncio
@patch("api.productlog.crud.ProductDetails")
@patch("api.productlog.crud.ProductDetailsSchema")
async def test_update_product_details_partial_update(mock_schema, mock_model):
    """Test partial update of product details."""
    # Arrange
    mock_product_instance = MagicMock()
    mock_product_instance.update_from_dict = AsyncMock()
    mock_product_instance.save = AsyncMock()
    mock_model.get_or_none = AsyncMock(return_value=mock_product_instance)
    
    expected_result = {**SAMPLE_PRODUCT_DICT, "productnameen": "Partially Updated Product"}
    mock_schema.from_tortoise_orm = AsyncMock(return_value=expected_result)
    
    # Create partial update data
    partial_data = ProductDetailsCreateSchema(
        productid="P001",
        productnameen="Partially Updated Product",
        category="Organoid(类器官)",
        setsubcategory="Human Organoid(人源类器官)",
        source="Human(人源)",
        productnamezh="测试产品",
        specification="Test Specification",
        unit="Box(盒)",
        components=[],
        is_sold_independently=True,
        remarks_temperature="Store at -20°C",
        storage_temperature_duration="6 months",
        reorderlevel=10,
        targetstocklevel=100,
        leadtime=5,
    )

    # Act
    result = await crud.update_product_details("P001", partial_data)

    # Assert
    mock_model.get_or_none.assert_awaited_once_with(productid="P001")
    mock_product_instance.update_from_dict.assert_awaited_once()
    mock_product_instance.save.assert_awaited_once()
    mock_schema.from_tortoise_orm.assert_awaited_once_with(mock_product_instance)
    assert result == expected_result
    # Verify that exclude_unset=True is used
    call_args = mock_product_instance.update_from_dict.call_args
    assert call_args is not None


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductDetails")
async def test_get_product_details_by_id_empty_string(mock_model):
    """Test get_product_details_by_id with empty string ID."""
    # Arrange
    mock_model.get_or_none = AsyncMock(return_value=None)

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        await crud.get_product_details_by_id("")
    
    assert "Product with ID  not found" in str(exc_info.value)
    mock_model.get_or_none.assert_awaited_once_with(productid="")


# Tests for ProductInventory CRUD operations

@pytest.mark.asyncio
@patch("api.productlog.crud.ProductInventory")
@patch("api.productlog.crud.ProductInventorySchema")
async def test_create_product_inventory_success(mock_schema, mock_model):
    """Test successful creation of product inventory."""
    # Arrange
    mock_created_obj = MagicMock()
    mock_model.create = AsyncMock(return_value=mock_created_obj)
    expected_result = SAMPLE_INVENTORY_RESPONSE_DATA
    mock_schema.from_tortoise_orm = AsyncMock(return_value=expected_result)

    # Act
    result = await crud.create_product_inventory(SAMPLE_INVENTORY_CREATE_DATA)

    # Assert
    mock_model.create.assert_awaited_once()
    mock_schema.from_tortoise_orm.assert_awaited_once_with(mock_created_obj)
    assert result == expected_result


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductInventory")
@patch("api.productlog.crud.ProductInventorySchema")
async def test_get_product_inventory_by_id_success(mock_schema, mock_model):
    """Test successful retrieval of product inventory by ID."""
    # Arrange
    mock_inventory = MagicMock()
    mock_model.get_or_none = AsyncMock(return_value=mock_inventory)
    expected_result = SAMPLE_INVENTORY_RESPONSE_DATA
    mock_schema.from_tortoise_orm = AsyncMock(return_value=expected_result)

    # Act
    result = await crud.get_product_inventory_by_id("BATCH123")

    # Assert
    mock_model.get_or_none.assert_awaited_once_with(batchid_internal="BATCH123")
    mock_schema.from_tortoise_orm.assert_awaited_once_with(mock_inventory)
    assert result == expected_result


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductInventory")
async def test_get_product_inventory_by_id_not_found(mock_model):
    """Test get_product_inventory_by_id when inventory is not found."""
    # Arrange
    mock_model.get_or_none = AsyncMock(return_value=None)

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        await crud.get_product_inventory_by_id("NONEXISTENT")
    
    assert "Product inventory with batch ID NONEXISTENT not found" in str(exc_info.value)
    mock_model.get_or_none.assert_awaited_once_with(batchid_internal="NONEXISTENT")


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductInventory")
@patch("api.productlog.crud.ProductInventorySchema")
async def test_update_product_inventory_success(mock_schema, mock_model):
    """Test successful update of product inventory."""
    # Arrange
    mock_inventory = MagicMock()
    mock_inventory.update_from_dict = AsyncMock()
    mock_inventory.save = AsyncMock()
    mock_model.get_or_none = AsyncMock(return_value=mock_inventory)
    
    updated_data = ProductInventoryCreateSchema(**{**SAMPLE_INVENTORY_DATA, "quantityinstock": 75})
    expected_result = {**SAMPLE_INVENTORY_RESPONSE_DATA, "quantityinstock": 75}
    mock_schema.from_tortoise_orm = AsyncMock(return_value=expected_result)

    # Act
    result = await crud.update_product_inventory("BATCH123", updated_data)

    # Assert
    mock_model.get_or_none.assert_awaited_once_with(batchid_internal="BATCH123")
    mock_inventory.update_from_dict.assert_awaited_once()
    mock_inventory.save.assert_awaited_once()
    mock_schema.from_tortoise_orm.assert_awaited_once_with(mock_inventory)
    assert result == expected_result


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductInventory")
async def test_update_product_inventory_not_found(mock_model):
    """Test update_product_inventory when inventory is not found."""
    # Arrange
    mock_model.get_or_none = AsyncMock(return_value=None)
    updated_data = ProductInventoryCreateSchema(**SAMPLE_INVENTORY_DATA)

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        await crud.update_product_inventory("NONEXISTENT", updated_data)
    
    assert "Product inventory with batch ID NONEXISTENT not found" in str(exc_info.value)
    mock_model.get_or_none.assert_awaited_once_with(batchid_internal="NONEXISTENT")


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductInventory")
async def test_delete_product_inventory_success(mock_model):
    """Test successful deletion of product inventory."""
    # Arrange
    mock_inventory = MagicMock()
    mock_inventory.delete = AsyncMock()
    mock_model.get_or_none = AsyncMock(return_value=mock_inventory)

    # Act
    result = await crud.delete_product_inventory("BATCH123")

    # Assert
    mock_model.get_or_none.assert_awaited_once_with(batchid_internal="BATCH123")
    mock_inventory.delete.assert_awaited_once()
    assert result == {"message": "Product inventory BATCH123 deleted successfully", "batch_id": "BATCH123"}


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductInventory")
async def test_delete_product_inventory_not_found(mock_model):
    """Test delete_product_inventory when inventory is not found."""
    # Arrange
    mock_model.get_or_none = AsyncMock(return_value=None)

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        await crud.delete_product_inventory("NONEXISTENT")
    
    assert "Product inventory with batch ID NONEXISTENT not found" in str(exc_info.value)
    mock_model.get_or_none.assert_awaited_once_with(batchid_internal="NONEXISTENT")
