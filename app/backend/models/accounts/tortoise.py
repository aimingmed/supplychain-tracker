from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import Optional

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, validator
from email_validator import validate_email, EmailNotValidError

class UsersAccount(models.Model):
    username = fields.CharField(max_length=50, pk=True)
    password = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
UsersAccountSchema = pydantic_model_creator(UsersAccount)
