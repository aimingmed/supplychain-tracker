from typing import List, Union

from fastapi import HTTPException, status

from models.accounts.pydantic import AccountPayloadSchema
from models.accounts.tortoise import UsersAccount
from models.requests.authentication import AuthHandler

# instantiate the Auth Handler
auth_handler = AuthHandler()


async def create_account(payload: AccountPayloadSchema) -> int:
    """Create a new user account.

    Args:
        payload (AccountPayloadSchema): The account information.

    Raises:
        HTTPException: If the username or email already exists.

    Returns:
        int: The username of the created account.
    """
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
    existing_account = await UsersAccount.filter(username=account.username).first()
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    # Check if the email already exists
    existing_email = await UsersAccount.filter(email=account.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )
    await account.save()
    return account.username


async def get(username: str) -> Union[dict, None]:
    """Retrieve a user account by username.

    Args:
        username (str): The username of the account to retrieve.

    Returns:
        Union[dict, None]: The account information or None if not found.
    """
    account = await UsersAccount.filter(username=username).first().values()
    if account:
        return account
    return None


async def get_all() -> List:
    """Retrieve all user accounts.

    Returns:
        List: A list of all user accounts.
    """
    accounts = await UsersAccount.all().values()
    return accounts
