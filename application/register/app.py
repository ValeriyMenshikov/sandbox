from fastapi import FastAPI, APIRouter, Depends, status, Response

from application.clients.http.dm_api_account.models.api_models import UserEnvelope
from application.clients.http.dm_api_account.apis.account_api import AccountApi, Registration
from application.dependency.dependency import get_http_account_api

app = FastAPI(title="Register API")
router = APIRouter(prefix="/user", tags=["User"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
        registration: Registration,
        account_api: AccountApi = Depends(get_http_account_api)
) -> None:
    await account_api.post_v1_account(registration=registration)


@router.put("/activate")
async def activate(
        token: str,
        account_api: AccountApi = Depends(get_http_account_api)
) -> UserEnvelope:
    return await account_api.put_v1_account_token(token=token)


app.include_router(router)
