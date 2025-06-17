from typing import List, Union

from models.accounts.pydantic import AccountPayloadSchema
from models.accounts.tortoise import UsersAccount


async def register(payload: AccountPayloadSchema) -> int:
    account = UsersAccount(
        username=payload.username.lower(),
        email=payload.email.lower(),
        password=payload.password,
        list_of_roles=payload.list_of_roles,
        last_login=payload.last_login
    )
    await account.save()
    return account.id


async def get(id: int) -> Union[dict, None]:
    account = await UsersAccount.filter(id=id).first().values()
    if account:
        return account
    return None


async def get_all() -> List:
    accounts = await UsersAccount.all().values()
    return accounts
