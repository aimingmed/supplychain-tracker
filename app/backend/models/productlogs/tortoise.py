from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import Optional

from datetime import datetime
from enum import Enum
from app.backend.models.basemodel import BaseModel, EmailStr, Field, validator
from email_validator import validate_email, EmailNotValidError


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


# SummarySchema = pydantic_model_creator(TextSummary)
