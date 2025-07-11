from unittest.mock import AsyncMock, patch

import pytest

from api.productlog import crud


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductDetails")
@patch("api.productlog.crud.ProductDetailsSchema")
async def test_get_all_product_details(mock_schema, mock_model):
    # Arrange
    mock_qs = AsyncMock()
    mock_model.all.return_value = mock_qs
    mock_schema.from_queryset = AsyncMock(return_value=[{"productid": "P1"}])

    # Act
    result = await crud.get_all_product_details()

    # Assert
    mock_schema.from_queryset.assert_awaited_once_with(mock_model.all())
    assert isinstance(result, list)
    assert result[0]["productid"] == "P1"


@pytest.mark.asyncio
@patch("api.productlog.crud.ProductInventory")
@patch("api.productlog.crud.ProductInventorySchema")
async def test_get_all_product_inventory(mock_schema, mock_model):
    # Arrange
    mock_qs = AsyncMock()
    mock_model.all.return_value = mock_qs
    mock_schema.from_queryset = AsyncMock(return_value=[{"batchid_internal": "B1"}])

    # Act
    result = await crud.get_all_product_inventory()

    # Assert
    mock_schema.from_queryset.assert_awaited_once_with(mock_model.all())
    assert isinstance(result, list)
    assert result[0]["batchid_internal"] == "B1"
