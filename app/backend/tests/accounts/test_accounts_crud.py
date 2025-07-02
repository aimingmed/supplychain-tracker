import importlib
import sys
import types
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

sys.modules["models.accounts.pydantic"] = types.SimpleNamespace(
    AccountPayloadSchema=MagicMock()
)
sys.modules["models.accounts.tortoise"] = types.SimpleNamespace(
    UsersAccount=MagicMock()
)
sys.modules["models.requests.authentication"] = types.SimpleNamespace(
    AuthHandler=MagicMock()
)

crud = importlib.import_module("api.accounts.crud")


@pytest.mark.asyncio
@patch("api.accounts.crud.UsersAccount")
@patch("api.accounts.crud.auth_handler")
async def test_create_account_success(mock_auth_handler, mock_UsersAccount):
    # Arrange
    payload = MagicMock()
    payload.username = "TestUser"
    payload.email = "test@example.com"
    payload.password = "password123"
    payload.list_of_roles = ["user"]
    payload.created_at = "2024-01-01T00:00:00Z"
    payload.is_verified = False
    payload.last_login = None

    mock_account_instance = MagicMock()
    mock_account_instance.username = payload.username.lower()
    mock_account_instance.email = payload.email.lower()
    mock_account_instance.save = AsyncMock()

    mock_UsersAccount.return_value = mock_account_instance
    mock_UsersAccount.filter.return_value.first = AsyncMock(side_effect=[None, None])
    mock_auth_handler.get_password_hash.return_value = "hashedpassword"

    # Act
    result = await crud.create_account(payload)

    # Assert
    assert result == payload.username.lower()
    mock_account_instance.save.assert_awaited_once()


@pytest.mark.asyncio
@patch("api.accounts.crud.UsersAccount")
@patch("api.accounts.crud.auth_handler")
async def test_create_account_username_exists(mock_auth_handler, mock_UsersAccount):
    payload = MagicMock()
    payload.username = "TestUser"
    payload.email = "test@example.com"
    payload.password = "password123"
    payload.list_of_roles = ["user"]
    payload.created_at = "2024-01-01T00:00:00Z"
    payload.is_verified = False
    payload.last_login = None

    mock_account_instance = MagicMock()
    mock_account_instance.username = payload.username.lower()
    mock_account_instance.email = payload.email.lower()
    mock_UsersAccount.return_value = mock_account_instance
    # Username exists
    mock_UsersAccount.filter.return_value.first = AsyncMock(side_effect=[True])
    mock_auth_handler.get_password_hash.return_value = "hashedpassword"

    with pytest.raises(crud.HTTPException) as exc:
        await crud.create_account(payload)
    assert exc.value.status_code == crud.status.HTTP_400_BAD_REQUEST
    assert "Username already exists" in str(exc.value.detail)


@pytest.mark.asyncio
@patch("api.accounts.crud.UsersAccount")
@patch("api.accounts.crud.auth_handler")
async def test_create_account_email_exists(mock_auth_handler, mock_UsersAccount):
    payload = MagicMock()
    payload.username = "TestUser"
    payload.email = "test@example.com"
    payload.password = "password123"
    payload.list_of_roles = ["user"]
    payload.created_at = "2024-01-01T00:00:00Z"
    payload.is_verified = False
    payload.last_login = None

    mock_account_instance = MagicMock()
    mock_account_instance.username = payload.username.lower()
    mock_account_instance.email = payload.email.lower()
    mock_UsersAccount.return_value = mock_account_instance
    # Username does not exist, email exists
    mock_UsersAccount.filter.return_value.first = AsyncMock(side_effect=[None, True])
    mock_auth_handler.get_password_hash.return_value = "hashedpassword"

    with pytest.raises(crud.HTTPException) as exc:
        await crud.create_account(payload)
    assert exc.value.status_code == crud.status.HTTP_400_BAD_REQUEST
    assert "Email already exists" in str(exc.value.detail)


@pytest.mark.asyncio
@patch("api.accounts.crud.UsersAccount")
async def test_get_found(mock_UsersAccount):
    username = "testuser"
    expected_account = {"username": username}
    mock_filter = MagicMock()
    mock_filter.first.return_value.values = AsyncMock(return_value=expected_account)
    mock_UsersAccount.filter.return_value = mock_filter

    result = await crud.get(username)
    assert result == expected_account


@pytest.mark.asyncio
@patch("api.accounts.crud.UsersAccount")
async def test_get_not_found(mock_UsersAccount):
    username = "nouser"
    mock_filter = MagicMock()
    mock_filter.first.return_value.values = AsyncMock(return_value=None)
    mock_UsersAccount.filter.return_value = mock_filter

    result = await crud.get(username)
    assert result is None


@pytest.mark.asyncio
@patch("api.accounts.crud.UsersAccount")
async def test_get_all(mock_UsersAccount):
    expected_accounts = [{"username": "user1"}, {"username": "user2"}]
    mock_UsersAccount.all.return_value.values = AsyncMock(
        return_value=expected_accounts
    )

    result = await crud.get_all()
    assert result == expected_accounts
