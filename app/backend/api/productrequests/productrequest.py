from fastapi import APIRouter, HTTPException
from app.backend.api.productrequests import crud
from app.backend.models.productrequests.pydantic import RequestDetailsCreate, RequestDetailsSchema, RequestDetailsResponse
from typing import List

router = APIRouter()

@router.post("/requests/", response_model=RequestDetailsSchema)
async def create_request(request: RequestDetailsCreate):
    return await crud.create_request(request)

@router.get("/requests/{requestid}", response_model=RequestDetailsResponse)
async def get_request(requestid: int):
    try:
        return await crud.get_request(requestid)
    except Exception:
        raise HTTPException(status_code=404, detail="Request not found")

@router.get("/requests/", response_model=List[RequestDetailsResponse])
async def list_requests():
    return await crud.list_requests()

@router.put("/requests/{requestid}", response_model=RequestDetailsSchema)
async def update_request(requestid: int, request: RequestDetailsCreate):
    return await crud.update_request(requestid, request)

@router.delete("/requests/{requestid}")
async def delete_request(requestid: int):
    await crud.delete_request(requestid)
    return {"detail": "Request deleted"}
