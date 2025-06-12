from fastapi import APIRouter, Depends, status, FastAPI

from application.clients.http.dm_api_account.apis.account_api import AccountApi
from application.clients.http.dm_api_account.apis.login_api import LoginApi
from application.clients.http.dm_api_account.models.api_models import (
    ChangeEmail,
    ChangePassword,
    LoginCredentials,
    Registration,
    ResetPassword,
    UserDetailsEnvelope,
    UserEnvelope,
)
from application.dependency.dependency import get_http_account_api, get_http_login_api
from application.utils import service_error_handler

app = FastAPI(
    title="DM API Account",
)

account_router = APIRouter(
    tags=["Account"],
)

login_router = APIRouter(
    tags=["Login"],
)


@account_router.post(
    "/v1/account",
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    operation_id="Register",
)
async def register_user(
    registration: Registration,
    account_api: AccountApi = Depends(get_http_account_api),  # noqa: B008
) -> dict:
    async with service_error_handler():
        response = await account_api.post_v1_account(registration=registration)
        return {"status": "success", "status_code": response.status_code}


@account_router.get(
    "/v1/account",
    response_model=UserDetailsEnvelope,
    summary="Get current user",
    operation_id="GetCurrent",
)
async def get_current_user(
    x_dm_auth_token: str,
    account_api: AccountApi = Depends(get_http_account_api),  # noqa: B008
) -> UserDetailsEnvelope:
    async with service_error_handler():
        return await account_api.get_v1_account(x_dm_auth_token=x_dm_auth_token)


@account_router.put(
    "/v1/account/{token}",
    response_model=UserEnvelope,
    summary="Activate registered user",
    operation_id="Activate",
)
async def activate_user(
    token: str,
    account_api: AccountApi = Depends(get_http_account_api),  # noqa: B008
) -> UserEnvelope:
    async with service_error_handler():
        return await account_api.put_v1_account_token(token=token)


@account_router.put(
    "/v1/account/email",
    status_code=status.HTTP_200_OK,
    summary="Change registered user email",
    operation_id="ChangeEmail",
)
async def change_email(
    change_email_data: ChangeEmail,
    x_dm_auth_token: str,
    account_api: AccountApi = Depends(get_http_account_api),  # noqa: B008
) -> UserEnvelope:
    async with service_error_handler():
        response = await account_api.put_v1_account_email(
            change_email=change_email_data,
            x_dm_auth_token=x_dm_auth_token,
        )
        return response


@account_router.put(
    "/v1/account/password",
    status_code=status.HTTP_200_OK,
    summary="Change registered user password",
    operation_id="ChangePassword",
)
async def change_password(
    change_password_data: ChangePassword,
    x_dm_auth_token: str,
    account_api: AccountApi = Depends(get_http_account_api),  # noqa: B008
) -> UserEnvelope:
    async with service_error_handler():
        response = await account_api.put_v1_account_password(
            change_password=change_password_data,
            x_dm_auth_token=x_dm_auth_token,
        )
        return response


@account_router.post(
    "/v1/account/password",
    status_code=status.HTTP_200_OK,
    summary="Reset registered user password",
    operation_id="ResetPassword",
)
async def reset_password(
    reset_password_data: ResetPassword,
    account_api: AccountApi = Depends(get_http_account_api),  # noqa: B008
) -> UserEnvelope:
    async with service_error_handler():
        response = await account_api.post_v1_account_password(
            reset_password=reset_password_data,
        )
        return response


@login_router.post(
    "/v1/account/login",
    response_model=UserEnvelope,
    summary="Authenticate via credentials",
)
async def login(
    login_credentials: LoginCredentials,
    login_api: LoginApi = Depends(get_http_login_api),  # noqa: B008
) -> UserEnvelope:
    async with service_error_handler():
        return await login_api.post_v1_account_login(
            login_credentials=login_credentials,
        )


@login_router.delete(
    "/v1/account/login",
    status_code=status.HTTP_200_OK,
    summary="Logout as current user",
)
async def logout(
    x_dm_auth_token: str,
    login_api: LoginApi = Depends(get_http_login_api),  # noqa: B008
) -> dict:
    async with service_error_handler():
        response = await login_api.delete_v1_account_login(
            x_dm_auth_token=x_dm_auth_token,
        )
        return {"status": "success", "status_code": response.status_code}


@login_router.delete(
    "/v1/account/login/all",
    status_code=status.HTTP_200_OK,
    summary="Logout from all devices",
)
async def logout_all(
    x_dm_auth_token: str,
    login_api: LoginApi = Depends(get_http_login_api),  # noqa: B008
) -> dict:
    async with service_error_handler():
        response = await login_api.delete_v1_account_login_all(
            x_dm_auth_token=x_dm_auth_token,
        )
        return {"status": "success", "status_code": response.status_code}


app.include_router(account_router)
app.include_router(login_router)
