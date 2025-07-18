"""
Tests for product inventory validation functionality.
Tests the validation that ensures inventory items have matching productid in ProductDetails.
"""
import pytest
from unittest.mock import AsyncMock, patch
from datetime import date, datetime

from api.productlog.crud import create_product_inventory, update_product_inventory
from models.productlog.pydantic import ProductInventoryCreateSchema, InventoryStatus


class TestProductInventoryValidation:
    """Test validation logic for product inventory."""

    @pytest.mark.asyncio
    @patch("api.productlog.crud.ProductDetails")
    @patch("api.productlog.crud.ProductInventory")
    @patch("api.productlog.crud.ProductInventorySchema")
    async def test_create_inventory_with_valid_productid(self, mock_schema, mock_inventory, mock_details):
        """Test creating inventory with valid productid succeeds."""
        # Arrange
        mock_product = AsyncMock()
        mock_details.get_or_none = AsyncMock(return_value=mock_product)
        
        mock_created_inventory = AsyncMock()
        mock_inventory.create = AsyncMock(return_value=mock_created_inventory)
        
        mock_schema_result = {"productid": "P001", "basicmediumid": "BM001"}
        mock_schema.from_tortoise_orm = AsyncMock(return_value=mock_schema_result)
        
        data = ProductInventoryCreateSchema(
            productid="P001",
            basicmediumid="BM001",
            addictiveid="AD001",
            quantityinstock=50,
            productiondate=date.today(),
            imageurl="http://example.com/image.jpg",
            status=InventoryStatus.AVAILABLE,
            productiondatetime=datetime.now(),
            producedby="John Doe",
            lastupdatedby="Jane Doe",
        )
        
        # Act
        result = await create_product_inventory(data)
        
        # Assert
        assert result == mock_schema_result
        mock_details.get_or_none.assert_awaited_once_with(productid="P001")
        mock_inventory.create.assert_awaited_once()

    @pytest.mark.asyncio
    @patch("api.productlog.crud.ProductDetails")
    async def test_create_inventory_with_invalid_productid(self, mock_details):
        """Test creating inventory with invalid productid fails."""
        # Arrange
        mock_details.get_or_none = AsyncMock(return_value=None)
        
        data = ProductInventoryCreateSchema(
            productid="INVALID",
            basicmediumid="BM001",
            addictiveid="AD001",
            quantityinstock=50,
            productiondate=date.today(),
            imageurl="http://example.com/image.jpg",
            status=InventoryStatus.AVAILABLE,
            productiondatetime=datetime.now(),
            producedby="John Doe",
            lastupdatedby="Jane Doe",
        )
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            await create_product_inventory(data)
        
        assert "Product with ID INVALID not found in ProductDetails" in str(exc_info.value)
        mock_details.get_or_none.assert_awaited_once_with(productid="INVALID")

    @pytest.mark.asyncio
    @patch("api.productlog.crud.ProductDetails")
    @patch("api.productlog.crud.ProductInventory")
    @patch("api.productlog.crud.ProductInventorySchema")
    async def test_update_inventory_with_valid_productid(self, mock_schema, mock_inventory, mock_details):
        """Test updating inventory with valid productid succeeds."""
        # Arrange
        mock_existing_inventory = AsyncMock()
        mock_inventory.get_or_none = AsyncMock(return_value=mock_existing_inventory)
        
        mock_product = AsyncMock()
        mock_details.get_or_none = AsyncMock(return_value=mock_product)
        
        mock_schema_result = {"productid": "P002", "basicmediumid": "BM002"}
        mock_schema.from_tortoise_orm = AsyncMock(return_value=mock_schema_result)
        
        data = ProductInventoryCreateSchema(
            productid="P002",
            basicmediumid="BM002",
            addictiveid="AD002",
            quantityinstock=75,
            productiondate=date.today(),
            imageurl="http://example.com/image.jpg",
            status=InventoryStatus.AVAILABLE,
            productiondatetime=datetime.now(),
            producedby="John Doe",
            lastupdatedby="Jane Doe",
        )
        
        # Act
        result = await update_product_inventory("BATCH123", data)
        
        # Assert
        assert result == mock_schema_result
        mock_inventory.get_or_none.assert_awaited_once_with(batchid_internal="BATCH123")
        mock_details.get_or_none.assert_awaited_once_with(productid="P002")
        mock_existing_inventory.update_from_dict.assert_awaited_once()
        mock_existing_inventory.save.assert_awaited_once()

    @pytest.mark.asyncio
    @patch("api.productlog.crud.ProductDetails")
    @patch("api.productlog.crud.ProductInventory")
    async def test_update_inventory_with_invalid_productid(self, mock_inventory, mock_details):
        """Test updating inventory with invalid productid fails."""
        # Arrange
        mock_existing_inventory = AsyncMock()
        mock_inventory.get_or_none = AsyncMock(return_value=mock_existing_inventory)
        
        mock_details.get_or_none = AsyncMock(return_value=None)
        
        data = ProductInventoryCreateSchema(
            productid="INVALID",
            basicmediumid="BM001",
            addictiveid="AD001",
            quantityinstock=50,
            productiondate=date.today(),
            imageurl="http://example.com/image.jpg",
            status=InventoryStatus.AVAILABLE,
            productiondatetime=datetime.now(),
            producedby="John Doe",
            lastupdatedby="Jane Doe",
        )
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            await update_product_inventory("BATCH123", data)
        
        assert "Product with ID INVALID not found in ProductDetails" in str(exc_info.value)
        mock_inventory.get_or_none.assert_awaited_once_with(batchid_internal="BATCH123")
        mock_details.get_or_none.assert_awaited_once_with(productid="INVALID")