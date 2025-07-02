from app.backend.models.productrequests.tortoise import RequestDetails
from app.backend.models.productrequests.pydantic import RequestDetailsCreate, RequestDetailsSchema, RequestDetailsResponse, ProductDetailsInfo
from app.backend.models.productlog.tortoise import ProductDetails

async def create_request(data: RequestDetailsCreate) -> RequestDetailsSchema:
    obj = await RequestDetails.create(**data.dict())
    return await RequestDetailsSchema.from_tortoise_orm(obj)

async def get_request(requestid: int) -> RequestDetailsResponse:
    obj = await RequestDetails.get(requestid=requestid).prefetch_related('requestproductid')
    product = await ProductDetails.get(productid=obj.requestproductid_id)
    product_info = ProductDetailsInfo(
        productid=product.productid,
        productnamezh=product.productnamezh,
        productnameen=product.productnameen
    )
    return RequestDetailsResponse(
        requestid=obj.requestid,
        requestorname=obj.requestorname,
        requestdate=obj.requestdate,
        requestproductid=obj.requestproductid_id,
        product=product_info,
        requestunit=obj.requestunit,
        is_urgent=obj.is_urgent,
        remarks=obj.remarks,
        fullfillername=obj.fullfillername,
        fullfilldate=obj.fullfilldate
    )

async def list_requests() -> list[RequestDetailsResponse]:
    requests = await RequestDetails.all().prefetch_related('requestproductid')
    result = []
    for obj in requests:
        product = await ProductDetails.get(productid=obj.requestproductid_id)
        product_info = ProductDetailsInfo(
            productid=product.productid,
            productnamezh=product.productnamezh,
            productnameen=product.productnameen
        )
        result.append(RequestDetailsResponse(
            requestid=obj.requestid,
            requestorname=obj.requestorname,
            requestdate=obj.requestdate,
            requestproductid=obj.requestproductid_id,
            product=product_info,
            requestunit=obj.requestunit,
            is_urgent=obj.is_urgent,
            remarks=obj.remarks,
            fullfillername=obj.fullfillername,
            fullfilldate=obj.fullfilldate
        ))
    return result

async def update_request(requestid: int, data: RequestDetailsCreate) -> RequestDetailsSchema:
    await RequestDetails.filter(requestid=requestid).update(**data.dict())
    obj = await RequestDetails.get(requestid=requestid)
    return await RequestDetailsSchema.from_tortoise_orm(obj)

async def delete_request(requestid: int) -> None:
    await RequestDetails.filter(requestid=requestid).delete()
