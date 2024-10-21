from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Header, Query, Response, status

from application.clients.http.dm_api_account.models.api_models import (
    ChangeEmail,
    ChangePassword,
    ResetPassword,
    UserDetailsEnvelope,
    UserEnvelope,
)
from application.dependency.dependency import get_account_service
from application.services.account.exceptions import AuthorizationError, EmailNotRegisteredError
from application.services.account.service import AccountService

app = FastAPI(title="Account API")
router = APIRouter(prefix="/account", tags=["Account"])


@router.get("/info", summary="Получить информацию о пользователе", description="Получить информацию о пользователе")
async def get_info(
    token: Annotated[str | None, Header(description="Авторизационный токен")],
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> UserDetailsEnvelope:
    return await account_service.get_info(token=token)


@router.put("/info", summary="Изменить информацию о пользователе", description="Изменить информацию о пользователе")
async def update_info(
    token: Annotated[str | None, Header(description="Авторизационный токен")],
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> Response:
    await account_service.update_info(token=token)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.post("/reset-password", summary="Сбросить пароль", description="Сбросить пароль")
async def reset_password(
    reset_password_model: ResetPassword,
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> UserEnvelope:
    return await account_service.reset_password(reset_password_model=reset_password_model)


@router.put("/change-password", summary="Изменить пароль", description="Изменить пароль")
async def change_password(
    change_password_model: ChangePassword,
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> UserEnvelope:
    return await account_service.change_password(change_password_model=change_password_model)


@router.put("/change-email", summary="Изменить email", description="Изменить email")
async def change_email(
    change_mail_model: ChangeEmail,
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> UserEnvelope:
    return await account_service.change_email(change_mail_model=change_mail_model)


@router.delete(path="", summary="Удалить учетную запись", description="Удалить учетную запись")
async def delete_account(
    token: Annotated[str | None, Header(description="Авторизационный токен")],
    email: Annotated[str | None, Query(description="email учетной записи")],
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> Response:
    try:
        await account_service.delete_account(token=token, email=email)
    except AuthorizationError:
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED, content="Authorization failed", media_type="text/plain"
        )
    except EmailNotRegisteredError:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST, content="Email is not registered", media_type="text/plain"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    path="/confirmation-delete",
    summary="Подтвердить удаление учетной записи",
    description="Подтвердить удаление учетной записи",
)
async def confirmation_delete_account(
    token: Annotated[str | None, Header(description="Авторизационный токен")],
    delete_token: Annotated[str | None, Query(description="Токен для подтверждения удаления учетной записи")],
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> Response:
    try:
        response = await account_service.delete_account_by_token(token=token, delete_token=delete_token)
    except AuthorizationError:
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED, content="Authorization failed", media_type="text/plain"
        )

    if response == "ok":
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(
        status_code=status.HTTP_400_BAD_REQUEST, content="Bad token or token expired", media_type="text/plain"
    )


app.include_router(router)
