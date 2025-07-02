from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class RequestDetails(models.Model):
    requestid = fields.IntField(pk=True, description="需求号")  # Auto-incrementing primary key
    requestorname = fields.CharField(max_length=100, description="需求人姓名")
    requestdate = fields.DatetimeField(auto_now_add=True, description="需求日期")
    requestproductid = fields.ForeignKeyField(
        "models.ProductDetails", related_name="requests", description="需求产品号"
    )
    requestunit = fields.CharField(max_length=20, description="需求单位")
    is_urgent = fields.BooleanField(default=False, description="是否紧急请求")
    remarks = fields.CharField(max_length=100, description="备注信息")
    fullfillername = fields.CharField(max_length=100, null=True, description="完成者姓名")
    fullfilldate = fields.DatetimeField(null=True, description="完成日期")

    def __str__(self):
        return self.requestid
    
RequestDetailsSchema = pydantic_model_creator(RequestDetails, name="RequestDetailsSchema")