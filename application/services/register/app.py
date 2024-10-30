from fastapi import APIRouter, Depends, FastAPI, status, HTTPException

from application.clients.http.dm_api_account.apis.account_api import (
    AccountApi,
    Registration,
)
from application.clients.http.dm_api_account.models.api_models import UserEnvelope
from application.dependency.dependency import get_http_account_api, get_register_service
from application.services.register.exceptions import RegistrationError
from application.services.register.service import RegisterService

app = FastAPI(title="Register API")
router = APIRouter(prefix="/user", tags=["Account"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
        registration: Registration,
        register_service: RegisterService = Depends(get_register_service),  # noqa: B008
) -> None:
    try:
        await register_service.register(registration=registration)
    except RegistrationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.put("/activate")
async def activate(
        token: str,
        account_api: AccountApi = Depends(get_http_account_api),  # noqa: B008
) -> UserEnvelope:
    return await account_api.put_v1_account_token(token=token)


app.include_router(router)
