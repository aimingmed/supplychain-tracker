import sys
import types
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import status

from api.accounts.accounts import (
    HTTPException,
    create_account,
    get_current_user,
    login_account,
    reset_password,
)
from models.accounts.pydantic import (
    AccountPayloadSchema,
    AccountResponseSchema,
    LoginSchema,
)

sys.modules["models.accounts.pydantic"] = types.SimpleNamespace(
    AccountPayloadSchema=AccountPayloadSchema,
    AccountResponseSchema=AccountResponseSchema,
    LoginSchema=LoginSchema,
)
sys.modules["models.accounts.tortoise"] = types.SimpleNamespace(
    UsersAccount=MagicMock()
)
sys.modules["models.requests.authentication"] = types.SimpleNamespace(
    AuthHandler=MagicMock()
)


@pytest.mark.asyncio
@patch("api.accounts.accounts.crud.create_account", new_callable=AsyncMock)
async def test_create_account_success(mock_create_account):
    payload = MagicMock()
    payload.email = "test@example.com"
    payload.list_of_roles = ["user"]
    mock_create_account.return_value = "testuser"
    response = await create_account(payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.body
    mock_create_account.assert_awaited_once_with(payload)


@pytest.mark.asyncio
@patch("api.accounts.accounts.crud.get", new_callable=AsyncMock)
@patch("api.accounts.accounts.auth_handler")
async def test_login_account_success(mock_auth_handler, mock_crud_get):
    payload = MagicMock()
    payload.username = "testuser"
    payload.password = "password"
    account = {
        "username": "testuser",
        "password": "hashed",
        "list_of_roles": ["user"],
    }
    mock_crud_get.return_value = account
    mock_auth_handler.verify_password.return_value = True
    mock_auth_handler.encode_token.return_value = "token"
    with patch("api.accounts.accounts.UsersAccount") as mock_UsersAccount:
        mock_UsersAccount.filter.return_value.update = AsyncMock(return_value=1)
        response = await login_account(payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.body
    mock_crud_get.assert_awaited_once_with(payload.username)
    mock_auth_handler.verify_password.assert_called_once()
    mock_auth_handler.encode_token.assert_called_once()


@pytest.mark.asyncio
@patch("api.accounts.accounts.crud.get", new_callable=AsyncMock)
@patch("api.accounts.accounts.auth_handler")
async def test_login_account_not_found(mock_auth_handler, mock_crud_get):
    payload = MagicMock()
    payload.username = "nouser"
    payload.password = "password"
    mock_crud_get.return_value = None
    with pytest.raises(HTTPException) as exc:
        await login_account(payload)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
@patch("api.accounts.accounts.crud.get", new_callable=AsyncMock)
@patch("api.accounts.accounts.auth_handler")
async def test_login_account_invalid_password(mock_auth_handler, mock_crud_get):
    payload = MagicMock()
    payload.username = "testuser"
    payload.password = "wrong"
    account = {
        "username": "testuser",
        "password": "hashed",
        "list_of_roles": ["user"],
    }
    mock_crud_get.return_value = account
    mock_auth_handler.verify_password.return_value = False
    with pytest.raises(HTTPException) as exc:
        await login_account(payload)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
@patch("api.accounts.accounts.auth_handler")
@patch("api.accounts.accounts.UsersAccount")
async def test_reset_password_success(mock_UsersAccount, mock_auth_handler):
    mock_auth_handler.decode_verification_token.return_value = "testuser"
    mock_auth_handler.get_password_hash.return_value = "hashed"
    mock_UsersAccount.filter.return_value.update = AsyncMock(return_value=1)
    response = await reset_password(token="sometoken", new_password="newpassword123")
    assert response.status_code == status.HTTP_200_OK
    assert b"Password reset successfully" in response.body


@pytest.mark.asyncio
@patch("api.accounts.accounts.auth_handler")
async def test_reset_password_invalid_token(mock_auth_handler):
    mock_auth_handler.decode_verification_token.side_effect = Exception("bad token")
    with pytest.raises(HTTPException) as exc:
        await reset_password(token="badtoken", new_password="newpassword123")
    assert exc.value.status_code == 401


@pytest.mark.asyncio
@patch("api.accounts.accounts.auth_handler")
async def test_reset_password_short_password(mock_auth_handler):
    mock_auth_handler.decode_verification_token.return_value = "testuser"
    with pytest.raises(HTTPException) as exc:
        await reset_password(token="sometoken", new_password="short")
    assert exc.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@patch("api.accounts.accounts.auth_handler")
@patch("api.accounts.accounts.UsersAccount")
async def test_reset_password_account_not_found(mock_UsersAccount, mock_auth_handler):
    mock_auth_handler.decode_verification_token.return_value = "testuser"
    mock_auth_handler.get_password_hash.return_value = "hashed"
    mock_UsersAccount.filter.return_value.update = AsyncMock(return_value=0)
    with pytest.raises(HTTPException) as exc:
        await reset_password(token="sometoken", new_password="newpassword123")
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


@patch("api.accounts.accounts.crud.get", new_callable=AsyncMock)
@patch("api.accounts.accounts.auth_handler")
def test_get_current_user_success(mock_auth_handler, mock_crud_get):
    auth_details = {"user_id": "testuser"}
    account = {
        "username": "testuser",
        "email": "test@example.com",
        "list_of_roles": ["user"],
        "is_verified": True,
        "password": "hashed",
    }
    mock_crud_get.return_value = account
    import asyncio

    response = asyncio.run(get_current_user(auth_details=auth_details))
    assert response.status_code == status.HTTP_200_OK
    assert b"testuser" in response.body


@patch("api.accounts.accounts.crud.get", new_callable=AsyncMock)
@patch("api.accounts.accounts.auth_handler")
def test_get_current_user_not_found(mock_auth_handler, mock_crud_get):
    auth_details = {"user_id": "nouser"}
    mock_crud_get.return_value = None
    import asyncio

    with pytest.raises(HTTPException) as exc:
        asyncio.run(get_current_user(auth_details=auth_details))
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
