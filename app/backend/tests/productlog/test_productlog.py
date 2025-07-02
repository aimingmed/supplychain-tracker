from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.productlog.productlog import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


@pytest.mark.asyncio
@patch("api.productlog.productlog.get_all_product_details", new_callable=AsyncMock)
def test_read_all_product_details(mock_get_all):
    # Arrange
    mock_get_all.return_value = [
        {
            "productid": "P1",
            "category": "Organoid(类器官)",
            "setsubcategory": "Human Organoid(人源类器官)",
            "source": "Human(人源)",
            "productnameen": "Test EN",
            "productnamezh": "测试",
            "specification": "Spec",
            "unit": "Box(盒)",
            "components": [],
            "is_sold_independently": True,
            "remarks_temperature": "Store at -20°C",
            "storage_temperature_duration": "6 months",
            "reorderlevel": 10,
            "targetstocklevel": 100,
            "leadtime": 5,
        }
    ]
    # Act
    response = client.get("/product-details")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["productid"] == "P1"


@pytest.mark.asyncio
@patch("api.productlog.productlog.get_all_product_inventory", new_callable=AsyncMock)
def test_read_all_product_inventory(mock_get_all):
    # Arrange
    mock_get_all.return_value = [
        {
            "batchid_internal": "B1",
            "batchid_external": "B1",
            "basicmediumid": "BM001",
            "addictiveid": "AD001",
            "quantityinstock": 50,
            "productiondate": "2025-01-01T00:00:00",
            "imageurl": "http://example.com/image.jpg",
            "status": "AVAILABLE",
            "productiondatetime": "2025-01-01T12:00:00",
            "producedby": "John Doe",
            "to_show": True,
            "lastupdated": "2025-01-02T12:00:00",
            "lastupdatedby": "Jane Doe",
            # plus all ProductDetailsSchema fields...
            "productid": "P1",
            "category": "Organoid(类器官)",
            "setsubcategory": "Human Organoid(人源类器官)",
            "source": "Human(人源)",
            "productnameen": "Test EN",
            "productnamezh": "测试",
            "specification": "Spec",
            "unit": "Box(盒)",
            "components": [],
            "is_sold_independently": True,
            "remarks_temperature": "Store at -20°C",
            "storage_temperature_duration": "6 months",
            "reorderlevel": 10,
            "targetstocklevel": 100,
            "leadtime": 5,
        }
    ]
    # Act
    response = client.get("/product-inventory")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["batchid_internal"] == "B1"
    assert data[0]["productid"] == "P1"
