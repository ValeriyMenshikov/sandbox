from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Response, status

from application.clients.http.dm_api_account.apis.login_api import LoginApi
from application.clients.http.dm_api_account.models.api_models import (
    LoginCredentials,
    UserEnvelope,
)
from application.dependency.dependency import get_http_login_api
from application.utils import service_error_handler

app = FastAPI(title="Auth API")

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    path="/auth",
    summary="Авторизация",
    description="Метод для авторизации пользователя",
)
async def auth(
    login_credentials: LoginCredentials,
    login_api: LoginApi = Depends(get_http_login_api),  # noqa: B008
) -> UserEnvelope:
    async with service_error_handler():
        response = await login_api.post_v1_account_login_with_http_info(login_credentials=login_credentials)
    if response.status_code == 200:
        response_data = UserEnvelope.model_validate_json(response.content)
        response_data.metadata = {"token": response.headers.get("x-dm-auth-token")}
        return response_data
    raise HTTPException(status_code=response.status_code, detail=response.text)


@router.delete(
    path="/logout",
    summary="Выход",
    description="Метод для выхода пользователя",
)
async def logout(
    token: Annotated[str, Header(description="Авторизационный токен")],
    login_api: LoginApi = Depends(get_http_login_api),  # noqa: B008
) -> Response:
    async with service_error_handler(status_code=status.HTTP_401_UNAUTHORIZED):
        await login_api.delete_v1_account_login_with_http_info(x_dm_auth_token=token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    path="/logout/all",
    summary="Выход",
    description="Метод для выхода пользователя со всех устройств",
)
async def logout_all(
    token: Annotated[str, Header(description="Авторизационный токен")],
    login_api: LoginApi = Depends(get_http_login_api),  # noqa: B008
) -> Response:
    async with service_error_handler(status_code=status.HTTP_401_UNAUTHORIZED):
        await login_api.delete_v1_account_login_all_with_http_info(x_dm_auth_token=token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


app.include_router(router)
