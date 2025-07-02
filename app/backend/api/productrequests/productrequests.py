from typing import List

from fastapi import APIRouter, Depends, HTTPException
from api.productrequests import crud
from models.productrequests.pydantic import (
    RequestDetailsCreate, 
    RequestDetailsSchema, 
    RequestDetailsResponse,
    RequestStatusUpdate
)
from models.requests.authentication import AuthHandler
from datetime import datetime

router = APIRouter()
auth_handler = AuthHandler()

@router.post("/requests/", response_model=RequestDetailsResponse)
async def create_request(
    request: RequestDetailsCreate,
    auth_details=Depends(auth_handler.auth_wrapper)
):
    """Create a new product request.

    Args:
        request (RequestDetailsCreate): The details of the request to create.
        auth_details (dict, optional): Authentication details containing user roles and username. Defaults to Depends(auth_handler.auth_wrapper).

    Raises:
        HTTPException: If the user does not have permission to create a request.

    Returns:
        RequestDetailsResponse: The details of the created request.
    """

    list_of_roles = auth_details["list_of_roles"]
    if "REQUESTOR" not in list_of_roles:
        raise HTTPException(
            status_code=403, 
            detail="You do not have permission to create a request."
        )
    request.requestorname = auth_details["username"]
    
    # if remarks in request is "string", convert it to empty string
    if request.remarks == "string":
        request.remarks = ""

    # Create the request and return the enriched response (with product info)
    created = await crud.create_request(request)
    # Fetch the full response with product info
    return await crud.get_request(created.requestid)

@router.get("/requests/{requestid}", response_model=RequestDetailsResponse)
async def get_request(
    requestid: str,
    auth_details=Depends(auth_handler.auth_wrapper)):

    list_of_roles = auth_details["list_of_roles"]
    username = auth_details["username"]

    # Fetch the request to check ownership
    try:
        request_obj = await crud.get_request(requestid)
    except Exception:
        raise HTTPException(status_code=404, detail="Request not found")

    if "ADMIN" in list_of_roles:
        return request_obj

    if "REQUESTOR" in list_of_roles and request_obj.requestorname == username:
        return request_obj

    raise HTTPException(
        status_code=403,
        detail="You do not have permission to view this request."
    )

@router.get("/requests/", response_model=List[RequestDetailsResponse])
async def list_requests(
    auth_details=Depends(auth_handler.auth_wrapper)
):
    """List all product requests.

    Args:
        auth_details (dict, optional): Authentication details containing user roles and username. Defaults to Depends(auth_handler.auth_wrapper).

    Raises:
        HTTPException: If the user does not have permission to view requests.

    Returns:
        List[RequestDetailsResponse]: A list of all product requests.
    """

    list_of_roles = auth_details["list_of_roles"]
    if "ADMIN" not in list_of_roles and "PRODUCTION_MANAGER" not in list_of_roles:
        raise HTTPException(
            status_code=403, 
            detail="You do not have permission to view requests."
        )
    
    return await crud.list_requests()

@router.put("/requests/{requestid}", response_model=RequestDetailsSchema)
async def update_request(
    requestid: str, 
    request: RequestDetailsCreate,
    auth_details=Depends(auth_handler.auth_wrapper)
):
    """Update a product request.

    Args:
        requestid (str): The ID of the request to update.
        request (RequestDetailsCreate): The updated request details.
        auth_details (dict, optional): Authentication details containing user roles and username. Defaults to Depends(auth_handler.auth_wrapper).

    Raises:
        HTTPException: If the user does not have permission to update the request.
        HTTPException: If the request is not found.

    Returns:
        RequestDetailsSchema: The updated request details.
    """
    
    username = auth_details["username"]

    # if remarks in request is "string", convert it to empty string
    if request.remarks == "string":
        request.remarks = ""

    # Fetch the request to check ownership
    try:
        request_obj = await crud.get_request(requestid)
    except Exception:
        raise HTTPException(status_code=404, detail="Request not found")

    if any(role in auth_details["list_of_roles"] for role in ["ADMIN", "PRODUCTION_MANAGER"]):
        # Prevent changing the requestorname field if present in the update payload
        if hasattr(request, "requestorname"):
            request.requestorname = request_obj.requestorname
        return await crud.update_request(requestid, request)
    
    if request_obj.requestorname == username:
        return await crud.update_request(requestid, request)

    raise HTTPException(
        status_code=403,
        detail="You do not have permission to modify this request."
    )

@router.delete("/requests/{requestid}")
async def delete_request(
    requestid: str,
    auth_details=Depends(auth_handler.auth_wrapper)
):
    """Delete a request.

    Args:
        requestid (str): The ID of the request to delete.
        auth_details (dict, optional): Authentication details containing user roles,
            automatically provided by dependency injection.

    Raises:
        HTTPException: If the user does not have permission to delete the request.

    Returns:
        dict: A message indicating successful deletion.
    """
    
    list_of_roles = auth_details["list_of_roles"]

    if (
        "ADMIN" in list_of_roles
        or "PRODUCTION_MANAGER" in list_of_roles
    ):
        await crud.delete_request(requestid)
        return {"detail": "Request deleted"}

    raise HTTPException(
        status_code=403,
        detail="You do not have permission to delete this request."
    )

@router.put("/requests/{requestid}/approve", response_model=RequestDetailsSchema)
async def update_request_approval(
    requestid: str, 
    auth_details=Depends(auth_handler.auth_wrapper)):
    """Approve a request.

    Args:
        requestid (str): The ID of the request to approve.
        auth_details (dict, optional): Authentication details containing user roles,
            automatically provided by dependency injection.

    Raises:
        HTTPException: If the user does not have permission to approve the request.
        HTTPException: If the request is not found.

    Returns:
        RequestDetailsSchema: The updated request details.
    """
    list_of_roles = auth_details["list_of_roles"]

    if "REQUEST_APPROVER" not in list_of_roles:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to approve a request."
        )

    # Update status and remarks
    username = auth_details["username"]
    request_obj = await crud.get_request(requestid)
    if not request_obj:
        raise HTTPException(status_code=404, detail="Request not found")

    existing_remarks = request_obj.remarks or ""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    if existing_remarks:
        remarks = f"{existing_remarks} | Approved by {username} at {timestamp}"
    else:
        remarks = f"Approved by {username} at {timestamp}"

    return await crud.update_request(
        requestid,
        RequestStatusUpdate(
            status="APPROVED",
            remarks=remarks
        )
    )

@router.put("/requests/{requestid}/reject", response_model=RequestDetailsSchema)
async def update_request_rejection(
    requestid: str,
    auth_details=Depends(auth_handler.auth_wrapper)):
    """Reject a request.

    Args:
        requestid (str): The ID of the request to reject.
        auth_details (dict, optional): Authentication details containing user roles,
            automatically provided by dependency injection.

    Raises:
        HTTPException: If the user does not have permission to reject the request.
        HTTPException: If the request is not found.

    Returns:
        RequestDetailsSchema: The updated request details.
    """
    list_of_roles = auth_details["list_of_roles"]

    if "REQUEST_APPROVER" not in list_of_roles:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to reject a request."
        )

    # Update status and remarks
    username = auth_details["username"]
    request_obj = await crud.get_request(requestid)
    if not request_obj:
        raise HTTPException(status_code=404, detail="Request not found")

    existing_remarks = request_obj.remarks or ""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    if existing_remarks:
        remarks = f"{existing_remarks} | Rejected by {username} at {timestamp}"
    else:
        remarks = f"Rejected by {username} at {timestamp}"

    return await crud.update_request(
        requestid,
        RequestStatusUpdate(
            status="REJECTED",
            remarks=remarks
        )
    )


@router.put("/requests/{requestid}/fullfill", response_model=RequestDetailsSchema)
async def fullfill_request(
    requestid: str,
    auth_details=Depends(auth_handler.auth_wrapper)):
    """Fullfill a request.

    Args:
        requestid (str): The ID of the request to fullfill.
        auth_details (dict, optional): Authentication details containing user roles,
            automatically provided by dependency injection.

    Raises:
        HTTPException: If the user does not have permission to fullfill the request.
        HTTPException: If the request is not found.
        HTTPException: If the request is already FULLFILLED or not in APPROVED status.

    Returns:
        RequestDetailsSchema: The updated request details.
    """
    
    list_of_roles = auth_details["list_of_roles"]

    if "FULFILLER" not in list_of_roles:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to fullfill a request."
        )

    # Update status and remarks
    username = auth_details["username"]
    request_obj = await crud.get_request(requestid)
    if not request_obj:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Check if the request is already FULLFILLED
    if request_obj.status == "FULLFILLED":
        raise HTTPException(
            status_code=400, 
            detail="Request is already FULLFILLED."
        )
    
    # If approved, we fullfill the request
    if request_obj.status != "APPROVED":
        raise HTTPException(
            status_code=400, 
            detail="Request is not in APPROVED status."
        )
    
    existing_remarks = request_obj.remarks or ""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    if existing_remarks:
        remarks = f"{existing_remarks} | Fullfilled by {username} at {timestamp}"
    else:
        remarks = f"Fullfilled by {username} at {timestamp}"

    return await crud.update_request(
        requestid,
        RequestStatusUpdate(
            status="FULLFILLED",
            remarks=remarks,
            fullfillername=username,
            fullfilldate=datetime.utcnow()
        )
    )
