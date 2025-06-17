from pydantic import BaseModel

from typing import List, Optional
from datetime import datetime
from enum import Enum

from email_validator import validate_email, EmailNotValidError
from pydantic import validator

class Role(str, Enum):
    ADMIN = "ADMIN"
    REQUESTOR = "REQUESTOR"
    SHIPPER = "SHIPPER"
    PRODUCER = "PRODUCER"
    PRODUCTION_MANAGER = "PRODUCTION_MANAGER"

class AccountPayloadSchema(BaseModel):
    username: str
    password: str
    email: str
    list_of_roles: Optional[List[Role]] = []
    last_login: Optional[datetime] = None

    @validator('email')
    def validate_email(cls, value: str) -> str:
        try:
            valid = validate_email(value)
            return valid.email
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email address: {e}")
        
    @validator('username')
    def validate_username(cls, value: str) -> str:
        if not value.isalnum() or len(value) < 3:
            raise ValueError("Username must be alphanumeric and at least 3 characters long.")
        return value
    
    @validator('password')
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return value
    
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
                "last_login": "2025-06-13T12:00:00"
            }
        }


