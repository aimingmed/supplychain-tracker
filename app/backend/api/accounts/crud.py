from typing import List, Union

from fastapi import APIRouter, Request, Body, status, HTTPException, Depends


from models.accounts.pydantic import AccountPayloadSchema
from models.accounts.tortoise import UsersAccount
from models.requests.authentication import AuthHandler

# instantiate the Auth Handler
auth_handler = AuthHandler()

async def create_account(payload: AccountPayloadSchema) -> int:
    account = UsersAccount(
        username=payload.username.lower(),
        email=payload.email.lower(),
        password=auth_handler.get_password_hash(payload.password),
        list_of_roles=payload.list_of_roles,
        created_at=payload.created_at,
        is_verified=payload.is_verified,
        last_login=payload.last_login,
    )

    # Check if the username already exists
    existing_account = await UsersAccount.filter(
        username=account.username
    ).first()
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Check if the email already exists
    existing_email = await UsersAccount.filter(
        email=account.email
    ).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    await account.save()
    return account.username


async def get(username: str) -> Union[dict, None]:
    account = await UsersAccount.filter(username=username).first().values()
    if account:
        return account
    return None


async def get_all() -> List:
    accounts = await UsersAccount.all().values()
    return accounts
