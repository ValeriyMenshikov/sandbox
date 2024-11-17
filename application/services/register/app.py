from fastapi import APIRouter, Depends, FastAPI, HTTPException, status

from application.clients.http.dm_api_account.apis.account_api import (
    AccountApi,
    Registration,
)
from application.clients.http.dm_api_account.models.api_models import UserEnvelope
from application.dependency.dependency import get_http_account_api, get_register_service
from application.services.register.exceptions import RegistrationError
from application.services.register.service import RegisterService
from application.utils import service_error_handler

app = FastAPI(title="Register API")
router = APIRouter(prefix="/user", tags=["Account"])


@router.post(
    path="/register",
    summary="Регистрация пользователя",
    description="""
    Метод для регистрации пользователя, после успешного выполнения на почтовый сервер будет отправлено письмо 
    для подтверждения регистрации, с помощью токена необходимо подтвердить регистрацию в методе activate""",  # noqa: W291
    status_code=status.HTTP_201_CREATED,
)
async def register(
    registration: Registration,
    register_service: RegisterService = Depends(get_register_service),  # noqa: B008
) -> None:
    async with service_error_handler():
        await register_service.register(registration=registration)


@router.put(
    path="/activate",
    summary="Подтвердить регистрацию",
    description="Метод для подтверждения регистрации пользователя с помощью токена из письма.",
)
async def activate(
    token: str,
    account_api: AccountApi = Depends(get_http_account_api),  # noqa: B008
) -> UserEnvelope:
    async with service_error_handler():
        response = await account_api.put_v1_account_token_with_http_info(token=token)
        return UserEnvelope.model_validate_json(response.content)


app.include_router(router)
