from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from api.productlog.productlog import router, auth_handler

app = FastAPI()
app.include_router(router)
client = TestClient(app)


# Sample test data
SAMPLE_PRODUCT_DETAILS = {
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

SAMPLE_PRODUCT_INVENTORY = {
    "productid": "P001",  # Added required productid field
    "basicmediumid": "BM001",
    "addictiveid": "AD001",
    "quantityinstock": 50,
    "productiondate": "2025-01-01",  # Fixed: use date format
    "imageurl": "http://example.com/image.jpg",
    "status": "AVAILABLE(可用)",  # Fixed: use correct enum value
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

SAMPLE_PRODUCT_INVENTORY_RESPONSE = {
    "batchid_internal": "BM001-AD001-ABC123",
    "batchid_external": "BM001-AD001",
    "lastupdated": "2025-01-02T12:00:00",
    "productid": "P001",  # Added required productid field
    "basicmediumid": "BM001",
    "addictiveid": "AD001",
    "quantityinstock": 50,
    "productiondate": "2025-01-01",
    "imageurl": "http://example.com/image.jpg",
    "status": "AVAILABLE(可用)",  # Fixed: use correct enum value
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

SAMPLE_AUTH_DETAILS = {
    "username": "testuser",
    "list_of_roles": ["ADMIN"]
}

SAMPLE_AUTH_DETAILS_PRODUCTION_MANAGER = {
    "username": "prodmanager",
    "list_of_roles": ["PRODUCTION_MANAGER"]
}

SAMPLE_AUTH_DETAILS_PRODUCER = {
    "username": "producer",
    "list_of_roles": ["PRODUCER"]
}

SAMPLE_AUTH_DETAILS_UNAUTHORIZED = {
    "username": "regularuser",
    "list_of_roles": ["USER"]
}


# Tests for GET /product-details
@patch("api.productlog.productlog.get_all_product_details", new_callable=AsyncMock)
def test_read_all_product_details_success(mock_get_all):
    """Test successful retrieval of all product details."""
    # Arrange
    mock_get_all.return_value = [SAMPLE_PRODUCT_DETAILS]
    
    # Act
    response = client.get("/product-details")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["productid"] == "P001"
    assert data[0]["productnameen"] == "Test Product EN"
    mock_get_all.assert_awaited_once()


@patch("api.productlog.productlog.get_all_product_details", new_callable=AsyncMock)
def test_read_all_product_details_empty(mock_get_all):
    """Test retrieval when no product details exist."""
    # Arrange
    mock_get_all.return_value = []
    
    # Act
    response = client.get("/product-details")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


# Tests for GET /product-inventory
@patch("api.productlog.productlog.get_all_product_inventory", new_callable=AsyncMock)
def test_read_all_product_inventory_success(mock_get_all):
    """Test successful retrieval of all product inventory."""
    # Arrange
    mock_get_all.return_value = [SAMPLE_PRODUCT_INVENTORY_RESPONSE]
    
    # Act
    response = client.get("/product-inventory")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["batchid_internal"] == "BM001-AD001-ABC123"
    assert data[0]["basicmediumid"] == "BM001"
    assert data[0]["addictiveid"] == "AD001"
    mock_get_all.assert_awaited_once()


# Tests for POST /product-details
@patch("api.productlog.productlog.create_product_details", new_callable=AsyncMock)
def test_create_product_details_success_admin(mock_create):
    """Test successful product creation by ADMIN user."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS
    mock_create.return_value = SAMPLE_PRODUCT_DETAILS
    
    # Act
    response = client.post("/product-details", json=SAMPLE_PRODUCT_DETAILS)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["productid"] == "P001"
    mock_create.assert_awaited_once()
    
    # Cleanup
    app.dependency_overrides.clear()


@patch("api.productlog.productlog.create_product_details", new_callable=AsyncMock)
def test_create_product_details_success_production_manager(mock_create):
    """Test successful product creation by PRODUCTION_MANAGER user."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS_PRODUCTION_MANAGER
    mock_create.return_value = SAMPLE_PRODUCT_DETAILS
    
    # Act
    response = client.post("/product-details", json=SAMPLE_PRODUCT_DETAILS)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["productid"] == "P001"
    mock_create.assert_awaited_once()
    
    # Cleanup
    app.dependency_overrides.clear()


def test_create_product_details_unauthorized():
    """Test product creation fails for unauthorized user."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS_UNAUTHORIZED
    
    # Act
    response = client.post("/product-details", json=SAMPLE_PRODUCT_DETAILS)
    
    # Assert
    assert response.status_code == 403
    data = response.json()
    assert "permission" in data["detail"]
    
    # Cleanup
    app.dependency_overrides.clear()


@patch("api.productlog.productlog.create_product_details", new_callable=AsyncMock)
def test_create_product_details_creation_error(mock_create):
    """Test product creation handles database errors."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS
    mock_create.side_effect = Exception("Database error")
    
    # Act
    response = client.post("/product-details", json=SAMPLE_PRODUCT_DETAILS)
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "Database error" in data["detail"]
    
    # Cleanup
    app.dependency_overrides.clear()


# Tests for GET /product-details/{product_id}
@patch("api.productlog.productlog.get_product_details_by_id", new_callable=AsyncMock)
def test_get_product_details_by_id_success(mock_get_by_id):
    """Test successful retrieval of product by ID."""
    # Arrange
    mock_get_by_id.return_value = SAMPLE_PRODUCT_DETAILS
    
    # Act
    response = client.get("/product-details/P001")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["productid"] == "P001"
    mock_get_by_id.assert_awaited_once_with("P001")


@patch("api.productlog.productlog.get_product_details_by_id", new_callable=AsyncMock)
def test_get_product_details_by_id_not_found(mock_get_by_id):
    """Test retrieval of non-existent product."""
    # Arrange
    mock_get_by_id.side_effect = ValueError("Product with ID NOTFOUND not found")
    
    # Act
    response = client.get("/product-details/NOTFOUND")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]


# Tests for PUT /product-details/{product_id}
@patch("api.productlog.productlog.update_product_details", new_callable=AsyncMock)
def test_update_product_details_success_admin(mock_update):
    """Test successful product update by ADMIN user."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS
    updated_product = {**SAMPLE_PRODUCT_DETAILS, "productnameen": "Updated Product"}
    mock_update.return_value = updated_product
    
    # Act
    response = client.put("/product-details/P001", json=updated_product)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["productnameen"] == "Updated Product"
    mock_update.assert_awaited_once()
    
    # Cleanup
    app.dependency_overrides.clear()


@patch("api.productlog.productlog.update_product_details", new_callable=AsyncMock)
def test_update_product_details_success_production_manager(mock_update):
    """Test successful product update by PRODUCTION_MANAGER user."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS_PRODUCTION_MANAGER
    mock_update.return_value = SAMPLE_PRODUCT_DETAILS
    
    # Act
    response = client.put("/product-details/P001", json=SAMPLE_PRODUCT_DETAILS)
    
    # Assert
    assert response.status_code == 200
    mock_update.assert_awaited_once()
    
    # Cleanup
    app.dependency_overrides.clear()


def test_update_product_details_unauthorized():
    """Test product update fails for unauthorized user."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS_UNAUTHORIZED
    
    # Act
    response = client.put("/product-details/P001", json=SAMPLE_PRODUCT_DETAILS)
    
    # Assert
    assert response.status_code == 403
    data = response.json()
    assert "permission" in data["detail"]
    
    # Cleanup
    app.dependency_overrides.clear()


@patch("api.productlog.productlog.update_product_details", new_callable=AsyncMock)
def test_update_product_details_not_found(mock_update):
    """Test product update handles non-existent product."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS
    mock_update.side_effect = ValueError("Product with ID NOTFOUND not found")
    
    # Act
    response = client.put("/product-details/NOTFOUND", json=SAMPLE_PRODUCT_DETAILS)
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]
    
    # Cleanup
    app.dependency_overrides.clear()


@patch("api.productlog.productlog.update_product_details", new_callable=AsyncMock)
def test_update_product_details_general_error(mock_update):
    """Test product update handles general errors."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS
    mock_update.side_effect = Exception("Database connection error")
    
    # Act
    response = client.put("/product-details/P001", json=SAMPLE_PRODUCT_DETAILS)
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "Database connection error" in data["detail"]
    
    # Cleanup
    app.dependency_overrides.clear()


# Tests for DELETE /product-details/{product_id}
@patch("api.productlog.productlog.delete_product_details", new_callable=AsyncMock)
def test_delete_product_details_success_admin(mock_delete):
    """Test successful product deletion by ADMIN user."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS
    mock_delete.return_value = {"message": "Product P001 deleted successfully", "product_id": "P001"}
    
    # Act
    response = client.delete("/product-details/P001")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product P001 deleted successfully"
    assert data["product_id"] == "P001"
    mock_delete.assert_awaited_once_with("P001")
    
    # Cleanup
    app.dependency_overrides.clear()


@patch("api.productlog.productlog.delete_product_details", new_callable=AsyncMock)
def test_delete_product_details_success_production_manager(mock_delete):
    """Test successful product deletion by PRODUCTION_MANAGER user."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS_PRODUCTION_MANAGER
    mock_delete.return_value = {"message": "Product P001 deleted successfully", "product_id": "P001"}
    
    # Act
    response = client.delete("/product-details/P001")
    
    # Assert
    assert response.status_code == 200
    mock_delete.assert_awaited_once()
    
    # Cleanup
    app.dependency_overrides.clear()


def test_delete_product_details_unauthorized():
    """Test product deletion fails for unauthorized user."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS_UNAUTHORIZED
    
    # Act
    response = client.delete("/product-details/P001")
    
    # Assert
    assert response.status_code == 403
    data = response.json()
    assert "permission" in data["detail"]
    
    # Cleanup
    app.dependency_overrides.clear()


@patch("api.productlog.productlog.delete_product_details", new_callable=AsyncMock)
def test_delete_product_details_not_found(mock_delete):
    """Test product deletion handles non-existent product."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS
    mock_delete.side_effect = ValueError("Product with ID NOTFOUND not found")
    
    # Act
    response = client.delete("/product-details/NOTFOUND")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]
    
    # Cleanup
    app.dependency_overrides.clear()


@patch("api.productlog.productlog.delete_product_details", new_callable=AsyncMock)
def test_delete_product_details_general_error(mock_delete):
    """Test product deletion handles general errors."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS
    mock_delete.side_effect = Exception("Database constraint violation")
    
    # Act
    response = client.delete("/product-details/P001")
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "Database constraint violation" in data["detail"]
    
    # Cleanup
    app.dependency_overrides.clear()
    data = response.json()
    assert "Database constraint violation" in data["detail"]


# Tests for ProductInventory API endpoints

# Tests for POST /product-inventory
@patch("api.productlog.productlog.create_product_inventory", new_callable=AsyncMock)
def test_create_product_inventory_success_admin(mock_create):
    """Test successful creation of product inventory by admin."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS
    mock_create.return_value = SAMPLE_PRODUCT_INVENTORY_RESPONSE
    
    # Act
    response = client.post("/product-inventory", json=SAMPLE_PRODUCT_INVENTORY)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["basicmediumid"] == "BM001"
    assert data["addictiveid"] == "AD001"
    assert "batchid_internal" in data
    
    # Cleanup
    app.dependency_overrides.clear()


@patch("api.productlog.productlog.create_product_inventory", new_callable=AsyncMock)
def test_create_product_inventory_success_producer(mock_create):
    """Test successful creation of product inventory by producer."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS_PRODUCER
    mock_create.return_value = SAMPLE_PRODUCT_INVENTORY_RESPONSE
    
    # Act
    response = client.post("/product-inventory", json=SAMPLE_PRODUCT_INVENTORY)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["basicmediumid"] == "BM001"
    
    # Cleanup
    app.dependency_overrides.clear()


def test_create_product_inventory_unauthorized():
    """Test product inventory creation fails for unauthorized user."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS_UNAUTHORIZED
    
    # Act
    response = client.post("/product-inventory", json=SAMPLE_PRODUCT_INVENTORY)
    
    # Assert
    assert response.status_code == 403
    data = response.json()
    assert "You do not have permission to create inventory" in data["detail"]
    
    # Cleanup
    app.dependency_overrides.clear()


# Tests for GET /product-inventory/{batch_id}
@patch("api.productlog.productlog.get_product_inventory_by_id", new_callable=AsyncMock)
def test_get_product_inventory_by_id_success(mock_get):
    """Test successful retrieval of product inventory by batch ID."""
    # Arrange
    mock_get.return_value = SAMPLE_PRODUCT_INVENTORY_RESPONSE
    
    # Act
    response = client.get("/product-inventory/BATCH123")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["basicmediumid"] == "BM001"
    assert data["addictiveid"] == "AD001"


@patch("api.productlog.productlog.get_product_inventory_by_id", new_callable=AsyncMock)
def test_get_product_inventory_by_id_not_found(mock_get):
    """Test product inventory retrieval when not found."""
    # Arrange
    mock_get.side_effect = ValueError("Product inventory with batch ID NONEXISTENT not found")
    
    # Act
    response = client.get("/product-inventory/NONEXISTENT")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Product inventory with batch ID NONEXISTENT not found" in data["detail"]


# Tests for PUT /product-inventory/{batch_id}
@patch("api.productlog.productlog.update_product_inventory", new_callable=AsyncMock)
def test_update_product_inventory_success(mock_update):
    """Test successful update of product inventory."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS
    updated_inventory = {**SAMPLE_PRODUCT_INVENTORY_RESPONSE, "quantityinstock": 75}
    mock_update.return_value = updated_inventory
    
    # Act
    response = client.put("/product-inventory/BATCH123", json={**SAMPLE_PRODUCT_INVENTORY, "quantityinstock": 75})
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["quantityinstock"] == 75
    
    # Cleanup
    app.dependency_overrides.clear()


@patch("api.productlog.productlog.update_product_inventory", new_callable=AsyncMock)
def test_update_product_inventory_unauthorized(mock_update):
    """Test product inventory update fails for unauthorized user."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS_UNAUTHORIZED
    
    # Act
    response = client.put("/product-inventory/BATCH123", json=SAMPLE_PRODUCT_INVENTORY)
    
    # Assert
    assert response.status_code == 403
    data = response.json()
    assert "You do not have permission to update inventory" in data["detail"]
    
    # Cleanup
    app.dependency_overrides.clear()


@patch("api.productlog.productlog.update_product_inventory", new_callable=AsyncMock)
def test_update_product_inventory_not_found(mock_update):
    """Test product inventory update when not found."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS
    mock_update.side_effect = ValueError("Product inventory with batch ID NONEXISTENT not found")
    
    # Act
    response = client.put("/product-inventory/NONEXISTENT", json=SAMPLE_PRODUCT_INVENTORY)
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Product inventory with batch ID NONEXISTENT not found" in data["detail"]
    
    # Cleanup
    app.dependency_overrides.clear()


# Tests for DELETE /product-inventory/{batch_id}
@patch("api.productlog.productlog.delete_product_inventory", new_callable=AsyncMock)
def test_delete_product_inventory_success(mock_delete):
    """Test successful deletion of product inventory."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS
    mock_delete.return_value = {"message": "Product inventory BATCH123 deleted successfully", "batch_id": "BATCH123"}
    
    # Act
    response = client.delete("/product-inventory/BATCH123")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product inventory BATCH123 deleted successfully"
    assert data["batch_id"] == "BATCH123"
    
    # Cleanup
    app.dependency_overrides.clear()


@patch("api.productlog.productlog.delete_product_inventory", new_callable=AsyncMock)
def test_delete_product_inventory_unauthorized(mock_delete):
    """Test product inventory deletion fails for unauthorized user."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS_UNAUTHORIZED
    
    # Act
    response = client.delete("/product-inventory/BATCH123")
    
    # Assert
    assert response.status_code == 403
    data = response.json()
    assert "You do not have permission to delete inventory" in data["detail"]
    
    # Cleanup
    app.dependency_overrides.clear()


@patch("api.productlog.productlog.delete_product_inventory", new_callable=AsyncMock)
def test_delete_product_inventory_not_found(mock_delete):
    """Test product inventory deletion when not found."""
    # Arrange
    app.dependency_overrides[auth_handler.auth_wrapper] = lambda: SAMPLE_AUTH_DETAILS
    mock_delete.side_effect = ValueError("Product inventory with batch ID NONEXISTENT not found")
    
    # Act
    response = client.delete("/product-inventory/NONEXISTENT")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Product inventory with batch ID NONEXISTENT not found" in data["detail"]
    
    # Cleanup
    app.dependency_overrides.clear()


# Tests for GET /product-inventory/by-product/{product_id}
@patch("api.productlog.productlog.get_product_inventory_by_product_id", new_callable=AsyncMock)
def test_get_product_inventory_by_product_id_success(mock_get):
    """Test successful retrieval of product inventory by product ID."""
    # Arrange
    mock_get.return_value = [SAMPLE_PRODUCT_INVENTORY_RESPONSE]
    
    # Act
    response = client.get("/product-inventory/by-product/P001")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["productid"] == "P001"
    assert data[0]["basicmediumid"] == "BM001"
    mock_get.assert_awaited_once_with("P001")


@patch("api.productlog.productlog.get_product_inventory_by_product_id", new_callable=AsyncMock)
def test_get_product_inventory_by_product_id_not_found(mock_get):
    """Test product inventory retrieval by product ID when product not found."""
    # Arrange
    mock_get.side_effect = ValueError("Product with ID INVALID not found in ProductDetails")
    
    # Act
    response = client.get("/product-inventory/by-product/INVALID")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Product with ID INVALID not found in ProductDetails" in data["detail"]
    mock_get.assert_awaited_once_with("INVALID")


@patch("api.productlog.productlog.get_product_inventory_by_product_id", new_callable=AsyncMock)
def test_get_product_inventory_by_product_id_empty(mock_get):
    """Test product inventory retrieval by product ID when no inventory exists."""
    # Arrange
    mock_get.return_value = []
    
    # Act
    response = client.get("/product-inventory/by-product/P002")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0
    mock_get.assert_awaited_once_with("P002")
