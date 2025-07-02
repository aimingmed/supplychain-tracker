from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import uuid
from datetime import datetime


class RequestDetails(models.Model):
    requestid = fields.CharField(
        max_length=32,
        pk=True,
        description="需求号",
        default=lambda: RequestDetails.generate_requestid()
    )
    requestorname = fields.CharField(max_length=100, description="需求人姓名")
    requestdate = fields.DatetimeField(auto_now_add=True, description="需求日期")
    requestproductid = fields.CharField(max_length=20, description="需求产品号 (ProductDetails.productid, application-level FK)")
    requestunit = fields.IntField(description="需求单位")
    is_urgent = fields.BooleanField(default=False, description="是否紧急请求")
    remarks = fields.CharField(max_length=4096, description="备注信息")
    status = fields.CharField(
        max_length=20,
        default="PENDING",
        description="请求状态 (PENDING, APPROVED, REJECTED, FULLFILLED)"
    )
    fullfillername = fields.CharField(max_length=100, null=True, description="完成者姓名")
    fullfilldate = fields.DatetimeField(null=True, description="完成日期")

    @staticmethod
    def generate_requestid():
        # Format: YYYYMMDDHHMMSS + 6 random hex digits
        dt_part = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        rand_part = uuid.uuid4().hex[:6]
        return f"{dt_part}{rand_part}"
    
    def __str__(self):
        return self.id

RequestDetailsSchema = pydantic_model_creator(RequestDetails, name="RequestDetailsSchema")