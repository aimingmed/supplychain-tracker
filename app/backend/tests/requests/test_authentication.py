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
    user_id = "user123"
    role = "admin"
    token = handler.encode_token(user_id, role)
    assert isinstance(token, str)
    decoded_user_id, decoded_role = handler.decode_token(token)
    assert decoded_user_id == user_id
    assert decoded_role == role


def test_decode_token_expired(monkeypatch):
    handler = auth_module.AuthHandler()
    user_id = "user123"
    role = "admin"
    # Create an expired token
    payload = {
        "exp": datetime.utcnow() - timedelta(minutes=1),
        "iat": datetime.utcnow() - timedelta(minutes=2),
        "sub": user_id,
        "role": role,
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
    user_id = "user123"
    role = "user"
    token = handler.encode_token(user_id, role)
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    result = handler.auth_wrapper(credentials)
    assert result["user_id"] == user_id
    assert result["role"] == role


def test_encode_and_decode_verification_token():
    handler = auth_module.AuthHandler()
    user_id = "verifyuser"
    token = handler.encode_verification_token(user_id)
    assert isinstance(token, str)
    decoded_user_id = handler.decode_verification_token(token)
    assert decoded_user_id == user_id


def test_decode_verification_token_expired():
    handler = auth_module.AuthHandler()
    user_id = "verifyuser"
    # Create an expired verification token
    payload = {
        "exp": datetime.utcnow() - timedelta(days=1),
        "iat": datetime.utcnow() - timedelta(days=2),
        "sub": user_id,
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
