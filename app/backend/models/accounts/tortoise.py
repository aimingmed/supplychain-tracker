from datetime import datetime
from typing import Optional

from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, EmailStr, Field, validator
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class UsersAccount(models.Model):
    username = fields.CharField(max_length=50, pk=True)
    password = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    list_of_roles = fields.JSONField(default=list)
    created_at = fields.DatetimeField(auto_now_add=True)
    is_verified = fields.BooleanField(default=False)
    last_login = fields.DatetimeField(null=True)

    def __str__(self):
        return self.username


UsersAccountSchema = pydantic_model_creator(UsersAccount)
