from typing import Annotated

from fastapi import FastAPI, APIRouter, Depends, status, Header
from application.clients.http.dm_api_account.models.api_models import UserEnvelope, UserDetailsEnvelope
from application.clients.http.dm_api_account.apis.account_api import AccountApi, Registration
from application.dependency.dependency import get_http_account_api

app = FastAPI(title="Account API")
router = APIRouter(prefix="/account", tags=["User"])


@router.get("/info")
async def get_info(
        token: Annotated[str | None, Header(description="Авторизационный токен")],
        account_api: AccountApi = Depends(get_http_account_api)
) -> UserDetailsEnvelope:
    return await account_api.get_v1_account(x_dm_auth_token=token)


app.include_router(router)
