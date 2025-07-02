from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ProductDetailsInfo(BaseModel):
    productid: str
    productnamezh: str
    productnameen: str


# Schema for reading a request (GET)
class RequestDetailsSchema(BaseModel):
    requestid: int = Field(..., description="需求号")
    requestorname: str = Field(..., max_length=100, description="需求人姓名")
    requestdate: datetime = Field(..., description="需求日期")
    requestproductid: str = Field(..., max_length=20, description="需求产品号 (ProductDetails.productid foreign key)")
    requestunit: str = Field(..., max_length=20, description="需求单位")
    is_urgent: bool = Field(default=False, description="是否紧急请求")
    remarks: str = Field(..., max_length=100, description="备注信息")
    fullfillername: Optional[str] = Field(None, max_length=100, description="完成者姓名")
    fullfilldate: Optional[datetime] = Field(None, description="完成日期")

# Schema for creating a new request (POST)
class RequestDetailsCreate(BaseModel):
    requestorname: str = Field(..., max_length=100, description="需求人姓名")
    requestproductid: str = Field(..., max_length=20, description="需求产品号 (ProductDetails.productid foreign key)")
    requestunit: str = Field(..., max_length=20, description="需求单位")
    is_urgent: bool = Field(default=False, description="是否紧急请求")
    remarks: str = Field(..., max_length=100, description="备注信息")
    fullfillername: Optional[str] = Field(None, max_length=100, description="完成者姓名")
    fullfilldate: Optional[datetime] = Field(None, description="完成日期")


class RequestDetailsResponse(BaseModel):
    requestid: int
    requestorname: str
    requestdate: datetime
    requestproductid: str
    product: ProductDetailsInfo
    requestunit: str
    is_urgent: bool
    remarks: str
    fullfillername: Optional[str]
    fullfilldate: Optional[datetime]