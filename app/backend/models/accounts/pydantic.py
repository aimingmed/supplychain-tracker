from typing import List, Optional
from datetime import datetime
from enum import Enum

from email_validator import validate_email, EmailNotValidError
from pydantic import BaseModel, EmailStr, Field, validator
from ..basemodel import SqlBaseModel

class Role(str, Enum):
    ADMIN = "ADMIN"
    REQUESTOR = "REQUESTOR"
    SHIPPER = "SHIPPER"
    PRODUCER = "PRODUCER"
    PRODUCTION_MANAGER = "PRODUCTION_MANAGER"


# Request payload schema (includes password)
class AccountPayloadSchema(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=50,
        description="Username must be alphanumeric and at least 3 characters long.",
        example="johndoe"
    )
    password: str = Field(
        ..., min_length=8,
        description="Password must be at least 8 characters long.",
        example="securepassword123"
    )
    email: str = EmailStr()
    list_of_roles: Optional[List[Role]] = ["ADMIN"]
    is_verified: bool = False
    created_at: Optional[datetime] = datetime.utcnow().isoformat()
    last_login: Optional[datetime] = datetime.utcnow().isoformat()

    @validator('email')
    def validate_email(cls, value: EmailStr) -> EmailStr:
        try:
            valid = validate_email(value)
            return valid.email
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email address: {e}")

    @validator('list_of_roles', each_item=True)
    def validate_roles(cls, value: Role) -> Role:
        if not isinstance(value, Role):
            raise ValueError(f"Invalid role: {value}. Must be one of {list(Role)}.")
        return value

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "securepassword123",
                "email": "johndoe@example.com",
                "list_of_roles": ["ADMIN", "REQUESTOR"],
                "is_verified": False,
                "created_at": "2025-06-13T12:00:00",
                "last_login": "2025-06-13T12:00:00"
            }
        }

# Response schema (does NOT include password)
class AccountResponseSchema(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=50,
        description="Username must be alphanumeric and at least 3 characters long."
    )
    email: str = EmailStr()
    list_of_roles: Optional[List[Role]] = []
    is_verified: bool = False
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "list_of_roles": ["ADMIN", "REQUESTOR"],
                "created_at": "2025-06-13T12:00:00",
                "is_verified": False,
                "last_login": "2025-06-13T12:00:00"
            }
        }


class LoginSchema(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=50,
        description="Username must be alphanumeric and at least 3 characters long.",
        example="johndoe"
    )
    password: str = Field(
        ..., min_length=8,
        description="Password must be at least 8 characters long.",
        example="securepassword123"
    )

    @validator('username')
    def validate_username(cls, value: str) -> str:
        if not value.isalnum() or len(value) < 3:
            raise ValueError(
                "Username must be alphanumeric and at least 3 characters long."
            )
        return value

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "securepassword123"
            }
        }

class CurrentUserSchema(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=50,
        description="Username must be alphanumeric and at least 3 characters long."
    )
    email: str = EmailStr()
    list_of_roles: List[Role]
    is_verified: bool = False

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "list_of_roles": ["ADMIN", "REQUESTOR"],
                "is_verified": False
            }
        }