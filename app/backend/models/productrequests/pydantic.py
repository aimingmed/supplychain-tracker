from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class ProductDetailsInfo(BaseModel):
    productid: str
    productnamezh: str
    productnameen: str

class RequestStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    FULLFILLED = "FULLFILLED"


# Schema for reading a request (GET)
class RequestDetailsSchema(BaseModel):
    requestid: str = Field(..., max_length=32, description="需求号")
    requestorname: str = Field(..., max_length=100, description="需求人姓名")
    requestdate: datetime = Field(..., description="需求日期")
    requestproductid: str = Field(..., max_length=20, description="需求产品号 (ProductDetails.productid foreign key)")
    requestunit: int = Field(..., description="需求单位", example=1)
    is_urgent: bool = Field(default=False, description="是否紧急请求")
    remarks: str = Field(..., max_length=4096, description="备注信息")
    status: RequestStatus = Field(..., description="请求状态 (PENDING, APPROVED, REJECTED, FULLFILLED)")
    fullfillername: Optional[str] = Field(None, max_length=100, description="完成者姓名")
    fullfilldate: Optional[datetime] = Field(None, description="完成日期")

# Schema for creating a new request (POST)
class RequestDetailsCreate(BaseModel):
    requestorname: str = Field(..., max_length=100, description="需求人姓名")
    requestdate: datetime = Field(default_factory=datetime.utcnow, description="需求日期")
    requestproductid: str = Field(..., max_length=20, description="需求产品号 (ProductDetails.productid foreign key)", example="P12345")
    requestunit: int = Field(..., description="需求单位", example=1)
    is_urgent: bool = Field(default=False, description="是否紧急请求")
    remarks: str = Field(..., max_length=4096, description="备注信息")

class RequestDetailsResponse(BaseModel):
    requestid: str
    requestorname: str
    requestdate: datetime
    requestproductid: str
    product: ProductDetailsInfo
    requestunit: int
    is_urgent: bool
    remarks: str
    status: RequestStatus
    fullfillername: Optional[str]
    fullfilldate: Optional[datetime]


# Schema for updating the status of a request (PUT)
class RequestStatusUpdate(BaseModel):
    status: RequestStatus = Field(..., description="请求状态 (PENDING, APPROVED, REJECTED, FULLFILLED)")
    remarks: Optional[str] = Field(None, max_length=4096, description="备注信息")
    fullfillername: Optional[str] = Field(None, max_length=100, description="完成者姓名")
    fullfilldate: Optional[datetime] = Field(None, description="完成日期")
