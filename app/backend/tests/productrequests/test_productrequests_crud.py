
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

import api.productrequests.crud as crud
from models.productrequests.pydantic import (
    RequestDetailsCreate,
    RequestDetailsResponse
)


@pytest.mark.asyncio
@patch("api.productrequests.crud.ProductDetails")
@patch("api.productrequests.crud.RequestDetails")
@patch("api.productrequests.crud.get_request")
async def test_create_request(mock_get_request, mock_RequestDetails, mock_ProductDetails):
    # Setup
    data = RequestDetailsCreate(
        requestorname="alice",
        requestdate=datetime.utcnow(),
        requestproductid="P123",
        requestunit=5,
        is_urgent=True,
        remarks="urgent request",
    )
    # Product exists
    mock_ProductDetails.get = AsyncMock()
    mock_RequestDetails.create = AsyncMock(return_value=MagicMock(requestid="REQ1"))
    mock_get_request.return_value = "response_obj"

    # Act
    result = await crud.create_request(data)

    # Assert
    mock_ProductDetails.get.assert_awaited_once_with(productid="P123")
    mock_RequestDetails.create.assert_awaited_once()
    mock_get_request.assert_awaited_once_with("REQ1")
    assert result == "response_obj"


@pytest.mark.asyncio
@patch("api.productrequests.crud.ProductDetails")
@patch("api.productrequests.crud.RequestDetails")
async def test_create_request_product_not_exist(mock_RequestDetails, mock_ProductDetails):
    data = RequestDetailsCreate(
        requestorname="alice",
        requestdate=datetime.utcnow(),
        requestproductid="P123",
        requestunit=5,
        is_urgent=True,
        remarks="urgent request",
    )
    # Product does not exist
    mock_ProductDetails.get = AsyncMock(side_effect=crud.DoesNotExist)

    with pytest.raises(crud.HTTPException) as exc:
        await crud.create_request(data)
    assert exc.value.status_code == 400
    assert "does not exist" in exc.value.detail


@pytest.mark.asyncio
@patch("api.productrequests.crud.ProductDetails")
@patch("api.productrequests.crud.RequestDetails")
async def test_get_request(mock_RequestDetails, mock_ProductDetails):
    # Setup
    mock_obj = MagicMock()
    mock_obj.requestid = "REQ1"
    mock_obj.requestorname = "alice"
    mock_obj.requestdate = datetime(2025, 7, 3, 12, 0, 0)
    mock_obj.requestproductid = "P123"
    mock_obj.requestunit = 5
    mock_obj.is_urgent = True
    mock_obj.remarks = "urgent"
    mock_obj.status = "PENDING"
    mock_obj.fullfillername = None
    mock_obj.fullfilldate = None
    mock_RequestDetails.get = AsyncMock(return_value=mock_obj)

    mock_product = MagicMock()
    mock_product.productid = "P123"
    mock_product.productnamezh = "产品"
    mock_product.productnameen = "Product"
    mock_ProductDetails.get = AsyncMock(return_value=mock_product)

    result = await crud.get_request("REQ1")
    assert isinstance(result, RequestDetailsResponse)
    assert result.requestid == "REQ1"
    assert result.product.productid == "P123"
    assert result.product.productnamezh == "产品"


@pytest.mark.asyncio
@patch("api.productrequests.crud.ProductDetails")
@patch("api.productrequests.crud.RequestDetails")
async def test_list_requests(mock_RequestDetails, mock_ProductDetails):
    # Setup
    mock_obj1 = MagicMock()
    mock_obj1.requestid = "REQ1"
    mock_obj1.requestorname = "alice"
    mock_obj1.requestdate = datetime(2025, 7, 3, 12, 0, 0)
    mock_obj1.requestproductid = "P123"
    mock_obj1.requestunit = 5
    mock_obj1.is_urgent = True
    mock_obj1.remarks = "urgent"
    mock_obj1.status = "PENDING"
    mock_obj1.fullfillername = None
    mock_obj1.fullfilldate = None

    mock_obj2 = MagicMock()
    mock_obj2.requestid = "REQ2"
    mock_obj2.requestorname = "bob"
    mock_obj2.requestdate = datetime(2025, 7, 3, 13, 0, 0)
    mock_obj2.requestproductid = "P124"
    mock_obj2.requestunit = 10
    mock_obj2.is_urgent = False
    mock_obj2.remarks = "normal"
    mock_obj2.status = "APPROVED"
    mock_obj2.fullfillername = "admin"
    mock_obj2.fullfilldate = datetime(2025, 7, 3, 14, 0, 0)

    mock_RequestDetails.all = AsyncMock(return_value=[mock_obj1, mock_obj2])

    def product_side_effect(productid):
        prod = MagicMock()
        prod.productid = productid
        prod.productnamezh = f"zh_{productid}"
        prod.productnameen = f"en_{productid}"
        return prod
    mock_ProductDetails.get = AsyncMock(side_effect=lambda productid: product_side_effect(productid))

    result = await crud.list_requests()
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].requestid == "REQ1"
    assert result[1].requestid == "REQ2"
    assert result[0].product.productid == "P123"
    assert result[1].product.productid == "P124"


@pytest.mark.asyncio
@patch("api.productrequests.crud.RequestDetails")
@patch("api.productrequests.crud.get_request")
async def test_update_request(mock_get_request, mock_RequestDetails):
    # Setup
    mock_RequestDetails.filter.return_value.update = AsyncMock()
    mock_RequestDetails.get = AsyncMock(return_value=MagicMock(requestid="REQ1"))
    mock_get_request.return_value = "updated_response"

    data = RequestDetailsCreate(
        requestorname="alice",
        requestdate=datetime.utcnow(),
        requestproductid="P123",
        requestunit=5,
        is_urgent=True,
        remarks="update",
    )

    result = await crud.update_request("REQ1", data)
    mock_RequestDetails.filter.assert_called_once_with(requestid="REQ1")
    mock_RequestDetails.filter.return_value.update.assert_awaited_once()
    mock_RequestDetails.get.assert_awaited_once_with(requestid="REQ1")
    mock_get_request.assert_awaited_once_with("REQ1")
    assert result == "updated_response"


@pytest.mark.asyncio
@patch("api.productrequests.crud.RequestDetails")
async def test_delete_request(mock_RequestDetails):
    mock_RequestDetails.filter.return_value.delete = AsyncMock()
    await crud.delete_request("REQ1")
    mock_RequestDetails.filter.assert_called_once_with(requestid="REQ1")
    mock_RequestDetails.filter.return_value.delete.assert_awaited_once()
