import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

# Import the router from your productrequests module
from api.productrequests.productrequests import router as productrequests_router
from api.productrequests import productrequests


# --- Auth Mocking ---
from fastapi import Depends

# This is the mock dependency to override auth_handler.auth_wrapper
def mock_auth_wrapper_requestor():
    return {"list_of_roles": ["REQUESTOR"], "username": "testuser"}

def mock_auth_wrapper_admin():
    return {"list_of_roles": ["ADMIN"], "username": "adminuser"}

def mock_auth_wrapper_approver():
    return {"list_of_roles": ["REQUEST_APPROVER"], "username": "approveruser"}

def mock_auth_wrapper_fulfiller():
    return {"list_of_roles": ["FULFILLER"], "username": "fulfilleruser"}

# Default: requestor
mock_auth = mock_auth_wrapper_requestor

productrequests.auth_handler.auth_wrapper = staticmethod(lambda: mock_auth())

app = FastAPI()
app.include_router(productrequests_router)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_openapi(client):
    # Basic test to check if the API is up and docs are available
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "paths" in response.json()


def test_list_requests_forbidden(client):
    # REQUESTOR role should not be able to list requests
    global mock_auth
    mock_auth = mock_auth_wrapper_requestor
    response = client.get("/requests/")
    assert response.status_code == 403

def test_list_requests_admin(client):
    # ADMIN role should be able to list requests (will fail if DB not set up, but checks auth logic)
    global mock_auth
    mock_auth = mock_auth_wrapper_admin
    response = client.get("/requests/")
    # 200 or 500 depending on DB, but not 403
    assert response.status_code != 403

def test_create_request_forbidden(client):
    # If not REQUESTOR, should be forbidden
    global mock_auth
    def forbidden_auth():
        return {"list_of_roles": ["OTHER_ROLE"], "username": "nobody"}
    mock_auth = forbidden_auth
    payload = {
        "requestorname": "should-be-ignored",
        "requestdate": "2025-07-03T12:00:00Z",
        "requestproductid": "P123",
        "requestunit": 1,
        "is_urgent": False,
        "remarks": "test"
    }
    response = client.post("/requests/", json=payload)
    assert response.status_code == 403

def test_create_request_missing_fields(client):
    # Should fail with 422 if required fields are missing
    global mock_auth
    mock_auth = mock_auth_wrapper_requestor
    payload = {"requestunit": 1}
    response = client.post("/requests/", json=payload)
    assert response.status_code == 422

# You can add more endpoint tests for update, approve, reject, fullfill, etc.,
# by switching mock_auth to the appropriate role and calling the endpoint.

# You can add more integration tests here, e.g.:
# def test_create_request_endpoint(client):
#     response = client.post("/requests/", json={...})
#     assert response.status_code == ...
