from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Query, Response, status
from httpx import HTTPStatusError
from starlette.responses import JSONResponse

from application.clients.http.dm_api_account.models.api_models import (
    ChangeEmail,
    ChangePassword,
    ResetPassword,
    UserDetailsEnvelope,
    UserEnvelope,
)
from application.dependency.dependency import get_account_service
from application.services.account.exceptions import AuthorizationError, EmailNotRegisteredError
from application.services.account.schema import UserSchema
from application.services.account.service import AccountService

app = FastAPI(title="Account API")
router = APIRouter(prefix="/account", tags=["Account"])


@router.get(
    path="/info",
    summary="Получить информацию о пользователе",
    description="Метод для получения информации о пользователе, метод кэширует данные на 20 секунд",
)
async def get_info(
    token: Annotated[str, Header(description="Авторизационный токен")],
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> UserDetailsEnvelope:
    return await account_service.get_info(token=token)


@router.patch(
    path="/info",
    summary="Изменить информацию о пользователе",
    description="Изменить информацию о пользователе",
)
async def update_info(
    token: Annotated[str, Header(description="Авторизационный токен")],
    user: UserSchema,
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> UserDetailsEnvelope:
    try:
        response = await account_service.update_info(token=token, user=user)
    except AuthorizationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed") from e
    return response


@router.post(
    path="/reset-password",
    summary="Сбросить пароль",
    description="Метод для сброса пароля, отправляет письмо с токеном для сброса пароля на почтовый сервер",
)
async def reset_password(
    reset_password_model: ResetPassword,
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> UserEnvelope:
    return await account_service.reset_password(reset_password_model=reset_password_model)


@router.put(
    path="/change-password",
    summary="Изменить пароль",
    description="""
    Метод позволяет изменить пароль пользователя, необходимо указать старый пароль и новый пароль, 
    а так же токен полученный в письме полученном после сброса пароля.
    """,  # noqa: W291
)
async def change_password(
    change_password_model: ChangePassword,
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> UserEnvelope:
    try:
        response = await account_service.change_password(change_password_model=change_password_model)
        return response
    except HTTPStatusError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.response.json()) from e


@router.put(
    path="/change-email",
    summary="Изменить email",
    description="Метод позволяет изменить почтовый адрес пользователя",
)
async def change_email(
    change_mail_model: ChangeEmail,
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> UserEnvelope:
    return await account_service.change_email(change_mail_model=change_mail_model)


@router.delete(
    path="",
    summary="Удалить учетную запись",
    description="""
    Метод запускает процесс удаления учетной записи пользователя, 
    после его выполнения на почту придет токен для подтверждения удаления учетной записи, 
    токен действует в течение 5 минут
    """,  # noqa: W291
)
async def delete_account(
    token: Annotated[str, Header(description="Авторизационный токен")],
    email: Annotated[str, Query(description="email учетной записи")],
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> JSONResponse:
    try:
        await account_service.delete_account(token=token, email=email)
    except AuthorizationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed") from e
    except EmailNotRegisteredError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is not registered") from e
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content={"message": "User has been started deletion account and expects confirmation by e-mail"},
    )


@router.delete(
    path="/confirmation-delete",
    summary="Подтвердить удаление учетной записи",
    description="Позволяет подтвердить и окончательно удалить учетную запись без возможности восстановления.",
)
async def confirmation_delete_account(
    token: Annotated[str, Header(description="Авторизационный токен")],
    delete_token: Annotated[str, Query(description="Токен для подтверждения удаления учетной записи")],
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> Response:
    try:
        response = await account_service.delete_account_by_token(token=token, delete_token=delete_token)
    except AuthorizationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed") from e

    if response == "ok":
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "User has been deleted"})
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad token or token expired")


app.include_router(router)
