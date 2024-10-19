from fastapi import FastAPI, APIRouter
from typing import Annotated

from fastapi import FastAPI, APIRouter, Depends, status, Header
from application.clients.http.dm_api_account.models.api_models import UserEnvelope, UserDetailsEnvelope, \
    LoginCredentials
from application.clients.http.dm_api_account.apis.login_api import LoginApi
from application.dependency.dependency import get_http_account_api, get_http_login_api

app = FastAPI(title="Auth API")

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/auth")
async def auth(
        login_credentials: LoginCredentials,
        login_api: LoginApi = Depends(get_http_login_api)
) -> UserEnvelope:
    return await login_api.post_v1_account_login(login_credentials=login_credentials)


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
        token: Annotated[str | None, Header(description="Авторизационный токен")],
        login_api: LoginApi = Depends(get_http_login_api)
) -> None:
    await login_api.delete_v1_account_login(x_dm_auth_token=token)


app.include_router(router)
