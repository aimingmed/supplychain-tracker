from typing import List

from fastapi import APIRouter, Request, Body, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from api.accounts import crud
from models.accounts.pydantic import (
    AccountPayloadSchema, 
    AccountResponseSchema,
    LoginSchema
    )
from models.accounts.tortoise import UsersAccount
from models.requests.authentication import AuthHandler
from datetime import datetime

router = APIRouter()


# instantiate the Auth Handler
auth_handler = AuthHandler()


@router.post("/register", response_model=AccountResponseSchema, status_code=201)
async def create_account(payload: AccountPayloadSchema) -> AccountResponseSchema:
    username = await crud.create_account(payload)

    response_object = {
        "username": username,
        "email": payload.email.lower(),
        "list_of_roles": payload.list_of_roles,
        "is_verified": False,
    }
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response_object)


@router.post("/login", response_model=AccountResponseSchema, status_code=200)
async def login_account(request: Request, payload: LoginSchema) -> JSONResponse:
    account = await crud.get(payload.username)

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )

    if not auth_handler.verify_password(payload.password, account["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Update last login time
    current_time = datetime.utcnow()  # Use datetime object, not string
    await UsersAccount.filter(username=payload.username).update(last_login=current_time)

    # Generate token
    token = auth_handler.encode_token(account["username"], account["list_of_roles"])

    return JSONResponse(status_code=status.HTTP_200_OK, content={"token": token})


# route to get the current user's account details
@router.get("/me", response_model=AccountResponseSchema, status_code=200)
async def get_current_user(
    auth_details=Depends(auth_handler.auth_wrapper),
) -> JSONResponse:
    # Use 'user_id' instead of 'username' as per auth_wrapper return value
    username = auth_details["user_id"]
    account = await crud.get(username)

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )

    response_object = {
        "username": account["username"],
        "email": account["email"],
        "list_of_roles": account["list_of_roles"],
        "is_verified": False,  # Assuming is_verified is always False for now
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_object)