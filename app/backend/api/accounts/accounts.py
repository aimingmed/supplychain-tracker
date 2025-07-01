from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from api.accounts import crud
from models.accounts.pydantic import (AccountPayloadSchema,
                                      AccountResponseSchema, LoginSchema)
from models.accounts.tortoise import UsersAccount
from models.requests.authentication import AuthHandler

router = APIRouter()

# instantiate the Auth Handler
auth_handler = AuthHandler()


@router.post("/register", response_model=AccountResponseSchema, status_code=201)
async def create_account(payload: AccountPayloadSchema) -> AccountResponseSchema:
    """Create a new user account.

    Args:
        payload (AccountPayloadSchema): The account information.

    Returns:
        AccountResponseSchema: The created account information.
    """
    username = await crud.create_account(payload)
    response_object = {
        "username": username,
        "email": payload.email.lower(),
        "list_of_roles": payload.list_of_roles,
        "is_verified": False,
    }
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response_object)


@router.post("/login", status_code=200)
async def login_account(payload: LoginSchema) -> JSONResponse:
    """Log in a user account.

    Args:
        payload (LoginSchema): The login credentials.

    Raises:
        HTTPException: If the account is not found.
        HTTPException: If the credentials are invalid.

    Returns:
        JSONResponse: The login response containing the token.
    """
    account = await crud.get(payload.username)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    if not auth_handler.verify_password(payload.password, account["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    # Update last login time
    current_time = datetime.utcnow()  # Use datetime object, not string
    await UsersAccount.filter(username=payload.username).update(last_login=current_time)
    # Generate token
    token = auth_handler.encode_token(account["username"], account["list_of_roles"])
    return JSONResponse(status_code=status.HTTP_200_OK, content={"token": token})


@router.post("/reset-password", response_description="Reset password", status_code=200)
async def reset_password(
    token: str = Body(...), new_password: str = Body(...)
) -> JSONResponse:
    """Reset the password for a user account.

    Args:
        token (str, optional): The reset token. Defaults to Body(...).
        new_password (str, optional): The new password. Defaults to Body(...).

    Raises:
        HTTPException: If the token is invalid.
        HTTPException: If the new password is too short.
        HTTPException: If the account is not found.

    Returns:
        JSONResponse: The response indicating the result of the password reset.
    """
    try:
        # Decode the token to get the username
        username = auth_handler.decode_verification_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    # Enforce minimum password length from AccountPayloadSchema
    min_password_length = 8  # Keep in sync with AccountPayloadSchema
    if len(new_password) < min_password_length:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"Password must be at least {min_password_length} " "characters long."
            ),
        )
    hashed_password = auth_handler.get_password_hash(new_password)
    # Update the password in the database
    updated_count = await UsersAccount.filter(username=username).update(
        password=hashed_password
    )
    if updated_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Password reset successfully"},
    )


@router.get("/me", response_model=AccountResponseSchema, status_code=200)
async def get_current_user(
    auth_details=Depends(auth_handler.auth_wrapper),
) -> JSONResponse:
    """Get the current user's account details.


    Args:
        auth_details (dict, optional): The authentication details.
            Defaults to Depends(auth_handler.auth_wrapper).

    Raises:
        HTTPException: If the account is not found.

    Returns:
        JSONResponse: The response containing the account details.
    """
    # Use 'user_id' instead of 'username' as per auth_wrapper return value
    username = auth_details["user_id"]
    account = await crud.get(username)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    # follow the same structure as the response model
    account = jsonable_encoder(account)
    # Create a response object without the password
    response_object = {
        "username": account["username"],
        "email": account["email"],
        "list_of_roles": account["list_of_roles"],
        "is_verified": account["is_verified"],
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_object)
