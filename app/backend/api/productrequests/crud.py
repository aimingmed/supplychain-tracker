from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from models.productlog.tortoise import ProductDetails
from models.productrequests.pydantic import (ProductDetailsInfo,
                                             RequestDetailsCreate,
                                             RequestDetailsResponse,
                                             RequestDetailsSchema)
from models.productrequests.tortoise import RequestDetails


async def create_request(data: RequestDetailsCreate) -> RequestDetailsSchema:
    data_dict = data.dict()
    # Check if the referenced product exists
    try:
        await ProductDetails.get(productid=data_dict["requestproductid"])
    except DoesNotExist:
        raise HTTPException(
            status_code=400,
            detail="ProductDetails with given productid does not exist.",
        )
    obj = await RequestDetails.create(**data_dict)
    # Always return the enriched response with all required fields
    return await get_request(obj.requestid)


async def get_request(requestid: int) -> RequestDetailsResponse:
    obj = await RequestDetails.get(requestid=requestid)
    product = await ProductDetails.get(productid=obj.requestproductid)
    product_info = ProductDetailsInfo(
        productid=product.productid,
        productnamezh=product.productnamezh,
        productnameen=product.productnameen,
    )
    return RequestDetailsResponse(
        requestid=obj.requestid,
        requestorname=obj.requestorname,
        requestdate=obj.requestdate,
        requestproductid=obj.requestproductid,
        product=product_info,
        requestunit=obj.requestunit,
        is_urgent=obj.is_urgent,
        remarks=obj.remarks,
        status=obj.status,
        fullfillername=obj.fullfillername,
        fullfilldate=obj.fullfilldate,
    )


async def list_requests() -> list[RequestDetailsResponse]:
    requests = await RequestDetails.all()
    result = []
    for obj in requests:
        product = await ProductDetails.get(productid=obj.requestproductid)
        product_info = ProductDetailsInfo(
            productid=product.productid,
            productnamezh=product.productnamezh,
            productnameen=product.productnameen,
        )
        result.append(
            RequestDetailsResponse(
                requestid=obj.requestid,
                requestorname=obj.requestorname,
                requestdate=obj.requestdate,
                requestproductid=obj.requestproductid,
                product=product_info,
                requestunit=obj.requestunit,
                is_urgent=obj.is_urgent,
                remarks=obj.remarks,
                status=obj.status,
                fullfillername=obj.fullfillername,
                fullfilldate=obj.fullfilldate,
            )
        )
    return result


async def update_request(
    requestid: int, data: RequestDetailsCreate
) -> RequestDetailsSchema:
    await RequestDetails.filter(requestid=requestid).update(**data.dict())
    obj = await RequestDetails.get(requestid=requestid)
    # Always return the enriched response with all required fields
    return await get_request(requestid)


async def delete_request(requestid: int) -> None:
    await RequestDetails.filter(requestid=requestid).delete()
