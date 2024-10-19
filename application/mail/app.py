from fastapi import FastAPI, APIRouter, Depends, Query

from application.clients.http.mailhog.apis.mailhog_api import MailhogApi
from application.clients.http.mailhog.models.models import Messages
from application.dependency.dependency import get_mailhog_api

app = FastAPI(title="Mail API")
router = APIRouter(prefix="/mail", tags=["Mail"])


@router.get("/messages")
async def get_messages(
        limit: int = Query(50, description="Количество необходимых записей", ge=1, le=100),
        mail_api: MailhogApi = Depends(get_mailhog_api)
) -> Messages:
    response = await mail_api.get_api_v2_messages(limit=limit)
    return response


@router.get("/search")
async def search(
        limit: int = Query(50, description="Количество необходимых записей", ge=1, le=100),
        kind: str = Query("containing", description="Тип поиска"),
        query: str = Query(None, description="Текст поиска"),
        start: int = Query(0, description="Начальная позиция поиска", ge=0),
        mail_api: MailhogApi = Depends(get_mailhog_api)
) -> Messages:
    response = await mail_api.get_api_v2_search(
        kind=kind, query=query, start=start, limit=limit)
    return response


app.include_router(router)
