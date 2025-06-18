from typing import List

from fastapi import APIRouter

from api.accounts import crud
from models.accounts.pydantic import AccountPayloadSchema, AccountResponseSchema
from models.accounts.tortoise import UsersAccountSchema

from models.requests.authentication import AuthHandler

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
        "last_login": None
    }
    return response_object