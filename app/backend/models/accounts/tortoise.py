from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import Optional

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, validator
from email_validator import validate_email, EmailNotValidError

class TextSummary(models.Model):
    url = fields.TextField()
    summary = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.url

class UsersAccount(models.Model):
    username = fields.CharField(max_length=50, pk=True)
    password = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    

class ProductDetails(models.Model):    
    productid = fields.CharField(max_length=20, pk=True)
    productname = fields.CharField(max_length=100)
    categoryname = fields.CharField(max_length=100)
    specification = fields.CharField(max_length=20)
    reorderlevel = fields.IntField()
    targetstocklevel = fields.IntField()
    leadtime = fields.IntField()

    def __str__(self):
        return self.productname

class ProductInventory(ProductDetails):
    batchid = fields.CharField(max_length=50)
    quantityinstock = fields.IntField()
    productiondate = fields.DateField()
    imageurl = fields.TextField()
    status = fields.CharField(max_length=20)
    lastupdated = fields.DatetimeField(auto_now=True)
    lastupdatedby = fields.CharField(max_length=50)


SummarySchema = pydantic_model_creator(TextSummary)
