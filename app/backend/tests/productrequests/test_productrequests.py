import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from fastapi.testclient import TestClient
from datetime import datetime

# Import the router to test
from api.productrequests import productrequests as pr

# Helper: mock auth_details
def make_auth_details(roles, username="user1"):
    return {"list_of_roles": roles, "username": username}

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.create_request", new_callable=AsyncMock)
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
async def test_create_request_success(mock_get_request, mock_create_request):
    req = MagicMock()
    req.remarks = "string"
    req.requestorname = ""
    req.requestid = "REQ1"
    mock_create_request.return_value = req
    mock_get_request.return_value = "response_obj"
    auth_details = make_auth_details(["REQUESTOR"], "alice")
    result = await pr.create_request(req, auth_details)
    assert result == "response_obj"
    assert req.requestorname == "alice"
    assert req.remarks == ""

@pytest.mark.asyncio
async def test_create_request_no_permission():
    req = MagicMock()
    auth_details = make_auth_details(["OTHER_ROLE"])
    with pytest.raises(HTTPException) as exc:
        await pr.create_request(req, auth_details)
    assert exc.value.status_code == 403

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
async def test_get_request_admin(mock_get_request):
    mock_get_request.return_value = MagicMock(requestorname="alice")
    auth_details = make_auth_details(["ADMIN"], "bob")
    result = await pr.get_request("REQ1", auth_details)
    assert result == mock_get_request.return_value

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
async def test_get_request_requestor(mock_get_request):
    mock_get_request.return_value = MagicMock(requestorname="bob")
    auth_details = make_auth_details(["REQUESTOR"], "bob")
    result = await pr.get_request("REQ1", auth_details)
    assert result == mock_get_request.return_value

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
async def test_get_request_forbidden(mock_get_request):
    mock_get_request.return_value = MagicMock(requestorname="alice")
    auth_details = make_auth_details(["REQUESTOR"], "bob")
    with pytest.raises(HTTPException) as exc:
        await pr.get_request("REQ1", auth_details)
    assert exc.value.status_code == 403

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
async def test_get_request_not_found(mock_get_request):
    mock_get_request.side_effect = Exception("not found")
    auth_details = make_auth_details(["ADMIN"])
    with pytest.raises(HTTPException) as exc:
        await pr.get_request("REQ1", auth_details)
    assert exc.value.status_code == 404

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.list_requests", new_callable=AsyncMock)
async def test_list_requests_admin(mock_list_requests):
    mock_list_requests.return_value = ["req1", "req2"]
    auth_details = make_auth_details(["ADMIN"])
    result = await pr.list_requests(auth_details)
    assert result == ["req1", "req2"]

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.list_requests", new_callable=AsyncMock)
async def test_list_requests_production_manager(mock_list_requests):
    mock_list_requests.return_value = ["req1"]
    auth_details = make_auth_details(["PRODUCTION_MANAGER"])
    result = await pr.list_requests(auth_details)
    assert result == ["req1"]

@pytest.mark.asyncio
async def test_list_requests_forbidden():
    auth_details = make_auth_details(["REQUESTOR"])
    with pytest.raises(HTTPException) as exc:
        await pr.list_requests(auth_details)
    assert exc.value.status_code == 403

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
@patch("api.productrequests.productrequests.crud.update_request", new_callable=AsyncMock)
async def test_update_request_admin(mock_update_request, mock_get_request):
    req = MagicMock()
    req.requestorname = "shouldnotchange"
    req.remarks = "string"
    mock_get_request.return_value = MagicMock(requestorname="alice")
    mock_update_request.return_value = "updated"
    auth_details = make_auth_details(["ADMIN"], "admin")
    result = await pr.update_request("REQ1", req, auth_details)
    assert result == "updated"
    assert req.requestorname == "alice"
    assert req.remarks == ""

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
@patch("api.productrequests.productrequests.crud.update_request", new_callable=AsyncMock)
async def test_update_request_owner(mock_update_request, mock_get_request):
    req = MagicMock()
    req.remarks = "string"
    mock_get_request.return_value = MagicMock(requestorname="bob")
    mock_update_request.return_value = "updated"
    auth_details = make_auth_details(["REQUESTOR"], "bob")
    result = await pr.update_request("REQ1", req, auth_details)
    assert result == "updated"
    assert req.remarks == ""

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
async def test_update_request_not_found(mock_get_request):
    req = MagicMock()
    mock_get_request.side_effect = Exception("not found")
    auth_details = make_auth_details(["ADMIN"])
    with pytest.raises(HTTPException) as exc:
        await pr.update_request("REQ1", req, auth_details)
    assert exc.value.status_code == 404

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
async def test_update_request_forbidden(mock_get_request):
    req = MagicMock()
    mock_get_request.return_value = MagicMock(requestorname="alice")
    auth_details = make_auth_details(["REQUESTOR"], "bob")
    with pytest.raises(HTTPException) as exc:
        await pr.update_request("REQ1", req, auth_details)
    assert exc.value.status_code == 403

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.delete_request", new_callable=AsyncMock)
async def test_delete_request_admin(mock_delete_request):
    auth_details = make_auth_details(["ADMIN"])
    result = await pr.delete_request("REQ1", auth_details)
    assert result == {"detail": "Request deleted"}
    mock_delete_request.assert_awaited_once_with("REQ1")

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.delete_request", new_callable=AsyncMock)
async def test_delete_request_production_manager(mock_delete_request):
    auth_details = make_auth_details(["PRODUCTION_MANAGER"])
    result = await pr.delete_request("REQ1", auth_details)
    assert result == {"detail": "Request deleted"}
    mock_delete_request.assert_awaited_once_with("REQ1")

@pytest.mark.asyncio
async def test_delete_request_forbidden():
    auth_details = make_auth_details(["REQUESTOR"])
    with pytest.raises(HTTPException) as exc:
        await pr.delete_request("REQ1", auth_details)
    assert exc.value.status_code == 403

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
@patch("api.productrequests.productrequests.crud.update_request", new_callable=AsyncMock)
async def test_update_request_approval_success(mock_update_request, mock_get_request):
    req_obj = MagicMock()
    req_obj.remarks = "remark"
    mock_get_request.return_value = req_obj
    mock_update_request.return_value = "updated"
    auth_details = make_auth_details(["REQUEST_APPROVER"], "approver")
    result = await pr.update_request_approval("REQ1", auth_details)
    assert result == "updated"
    mock_update_request.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_request_approval_forbidden():
    auth_details = make_auth_details(["REQUESTOR"])
    with pytest.raises(HTTPException) as exc:
        await pr.update_request_approval("REQ1", auth_details)
    assert exc.value.status_code == 403

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
async def test_update_request_approval_not_found(mock_get_request):
    mock_get_request.return_value = None
    auth_details = make_auth_details(["REQUEST_APPROVER"])
    with pytest.raises(HTTPException) as exc:
        await pr.update_request_approval("REQ1", auth_details)
    assert exc.value.status_code == 404

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
@patch("api.productrequests.productrequests.crud.update_request", new_callable=AsyncMock)
async def test_update_request_rejection_success(mock_update_request, mock_get_request):
    req_obj = MagicMock()
    req_obj.remarks = "remark"
    mock_get_request.return_value = req_obj
    mock_update_request.return_value = "updated"
    auth_details = make_auth_details(["REQUEST_APPROVER"], "approver")
    result = await pr.update_request_rejection("REQ1", auth_details)
    assert result == "updated"
    mock_update_request.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_request_rejection_forbidden():
    auth_details = make_auth_details(["REQUESTOR"])
    with pytest.raises(HTTPException) as exc:
        await pr.update_request_rejection("REQ1", auth_details)
    assert exc.value.status_code == 403

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
async def test_update_request_rejection_not_found(mock_get_request):
    mock_get_request.return_value = None
    auth_details = make_auth_details(["REQUEST_APPROVER"])
    with pytest.raises(HTTPException) as exc:
        await pr.update_request_rejection("REQ1", auth_details)
    assert exc.value.status_code == 404

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
@patch("api.productrequests.productrequests.crud.update_request", new_callable=AsyncMock)
async def test_fullfill_request_success(mock_update_request, mock_get_request):
    req_obj = MagicMock()
    req_obj.remarks = "remark"
    req_obj.status = "APPROVED"
    mock_get_request.return_value = req_obj
    mock_update_request.return_value = "updated"
    auth_details = make_auth_details(["FULFILLER"], "fulfiller")
    result = await pr.fullfill_request("REQ1", auth_details)
    assert result == "updated"
    mock_update_request.assert_awaited_once()

@pytest.mark.asyncio
async def test_fullfill_request_forbidden():
    auth_details = make_auth_details(["REQUESTOR"])
    with pytest.raises(HTTPException) as exc:
        await pr.fullfill_request("REQ1", auth_details)
    assert exc.value.status_code == 403

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
async def test_fullfill_request_not_found(mock_get_request):
    mock_get_request.return_value = None
    auth_details = make_auth_details(["FULFILLER"])
    with pytest.raises(HTTPException) as exc:
        await pr.fullfill_request("REQ1", auth_details)
    assert exc.value.status_code == 404

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
async def test_fullfill_request_already_fullfilled(mock_get_request):
    req_obj = MagicMock()
    req_obj.status = "FULLFILLED"
    mock_get_request.return_value = req_obj
    auth_details = make_auth_details(["FULFILLER"])
    with pytest.raises(HTTPException) as exc:
        await pr.fullfill_request("REQ1", auth_details)
    assert exc.value.status_code == 400
    assert "already FULLFILLED" in exc.value.detail

@pytest.mark.asyncio
@patch("api.productrequests.productrequests.crud.get_request", new_callable=AsyncMock)
async def test_fullfill_request_not_approved(mock_get_request):
    req_obj = MagicMock()
    req_obj.status = "PENDING"
    mock_get_request.return_value = req_obj
    auth_details = make_auth_details(["FULFILLER"])
    with pytest.raises(HTTPException) as exc:
        await pr.fullfill_request("REQ1", auth_details)
    assert exc.value.status_code == 400
    assert "not in APPROVED status" in exc.value.detail
