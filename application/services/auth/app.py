from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Header, Response, status

from application.clients.http.dm_api_account.apis.login_api import LoginApi
from application.clients.http.dm_api_account.models.api_models import (
    LoginCredentials,
    UserEnvelope,
)
from application.dependency.dependency import get_http_login_api

app = FastAPI(title="Auth API")

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/auth")
async def auth(
    login_credentials: LoginCredentials,
    login_api: LoginApi = Depends(get_http_login_api),  # noqa: B008
) -> UserEnvelope:
    return await login_api.post_v1_account_login(login_credentials=login_credentials)


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    token: Annotated[str | None, Header(description="Авторизационный токен")],
    login_api: LoginApi = Depends(get_http_login_api),  # noqa: B008
) -> Response:
    await login_api.delete_v1_account_login(x_dm_auth_token=token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/logout/all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(
    token: Annotated[str | None, Header(description="Авторизационный токен")],
    login_api: LoginApi = Depends(get_http_login_api),  # noqa: B008
) -> Response:
    await login_api.delete_v1_account_login_all(x_dm_auth_token=token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


app.include_router(router)
