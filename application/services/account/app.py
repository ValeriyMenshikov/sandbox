from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Header, Response, status

from application.clients.http.dm_api_account.models.api_models import (
    UserDetailsEnvelope,
)
from application.dependency.dependency import get_account_service
from application.services.account.service import AccountService

app = FastAPI(title="Account API")
router = APIRouter(prefix="/account", tags=["Account"])


@router.get("/info", description="Получить информацию о пользователе")
async def get_info(
    token: Annotated[str | None, Header(description="Авторизационный токен")],
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> UserDetailsEnvelope:
    return await account_service.account_api.get_v1_account(x_dm_auth_token=token)


@router.put("/info", description="Изменить информацию о пользователе")
async def update_info(
    token: Annotated[str | None, Header(description="Авторизационный токен")],
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> Response:
    await account_service.update_info(token=token)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.delete(path="", description="Удалить учетную запись")
async def delete_account(
    token: Annotated[str | None, Header(description="Авторизационный токен")],
    account_service: AccountService = Depends(get_account_service),  # noqa: B008
) -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


app.include_router(router)
