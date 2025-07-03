from datetime import datetime, timedelta

import jwt
import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

import models.requests.authentication as auth_module


class DummyAuth:
    def __init__(self, token):
        self.credentials = token


def test_get_password_hash_and_verify_password():
    handler = auth_module.AuthHandler()
    password = "testpassword123"
    hashed = handler.get_password_hash(password)
    assert isinstance(hashed, str)
    assert handler.verify_password(password, hashed)
    assert not handler.verify_password("wrongpassword", hashed)


def test_encode_and_decode_token():
    handler = auth_module.AuthHandler()
    username = "user123"
    list_of_roles = ["ADMIN", "REQUESTOR"]
    token = handler.encode_token(username, list_of_roles)
    assert isinstance(token, str)
    decoded_username, decoded_list_of_roles = handler.decode_token(token)
    assert decoded_username == username
    assert decoded_list_of_roles == list_of_roles


def test_decode_token_expired(monkeypatch):
    handler = auth_module.AuthHandler()
    username = "user123"
    list_of_roles = ["ADMIN", "REQUESTOR"]
    # Create an expired token
    payload = {
        "exp": datetime.utcnow() - timedelta(minutes=1),
        "iat": datetime.utcnow() - timedelta(minutes=2),
        "sub": username,
        "list_of_roles": list_of_roles,
    }
    token = jwt.encode(payload, handler.secret, algorithm="HS256")
    with pytest.raises(HTTPException) as excinfo:
        handler.decode_token(token)
    assert excinfo.value.status_code == 401
    assert "expired" in str(excinfo.value.detail)


def test_decode_token_invalid():
    handler = auth_module.AuthHandler()
    invalid_token = "invalid.token.value"
    with pytest.raises(HTTPException) as excinfo:
        handler.decode_token(invalid_token)
    assert excinfo.value.status_code == 401
    assert "Invalid token" in str(excinfo.value.detail)


def test_auth_wrapper():
    handler = auth_module.AuthHandler()
    username = "user123"
    list_of_roles = ["ADMIN", "REQUESTOR"]
    token = handler.encode_token(username, list_of_roles)
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    result = handler.auth_wrapper(credentials)
    assert result["username"] == username
    assert result["list_of_roles"] == list_of_roles


def test_encode_and_decode_verification_token():
    handler = auth_module.AuthHandler()
    username = "verifyuser"
    token = handler.encode_verification_token(username)
    assert isinstance(token, str)
    decoded_username = handler.decode_verification_token(token)
    assert decoded_username == username


def test_decode_verification_token_expired():
    handler = auth_module.AuthHandler()
    username = "verifyuser"
    # Create an expired verification token
    payload = {
        "exp": datetime.utcnow() - timedelta(days=1),
        "iat": datetime.utcnow() - timedelta(days=2),
        "sub": username,
    }
    token = jwt.encode(payload, handler.secret, algorithm="HS256")
    with pytest.raises(HTTPException) as excinfo:
        handler.decode_verification_token(token)
    assert excinfo.value.status_code == 401
    assert "expired" in str(excinfo.value.detail)


def test_decode_verification_token_invalid():
    handler = auth_module.AuthHandler()
    invalid_token = "invalid.token.value"
    with pytest.raises(HTTPException) as excinfo:
        handler.decode_verification_token(invalid_token)
    assert excinfo.value.status_code == 401
    assert "Invalid verification token" in str(excinfo.value.detail)
