from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Response, status

from application.clients.http.mailhog.apis.mailhog_api import MailhogApi
from application.clients.http.mailhog.models.models import Item, Messages
from application.dependency.dependency import get_mailhog_api
from application.services.mail.exceptions import MailNotFoundError

app = FastAPI(title="Mail API")
router = APIRouter(prefix="/mail", tags=["Mail"])


@router.get("/messages")
async def get_messages(
    limit: int = Query(50, description="Количество необходимых записей", ge=1, le=100),
    mail_api: MailhogApi = Depends(get_mailhog_api),  # noqa: B008
) -> Messages:
    response = await mail_api.get_api_v2_messages(limit=limit)
    return response


@router.get("/search")
async def search(
    limit: int = Query(50, description="Количество необходимых записей", ge=1, le=100),
    kind: str = Query("containing", description="Тип поиска"),
    query: str = Query(None, description="Текст поиска"),
    start: int = Query(0, description="Начальная позиция поиска", ge=0),
    mail_api: MailhogApi = Depends(get_mailhog_api),  # noqa: B008
) -> Messages:
    response = await mail_api.get_api_v2_search(kind=kind, query=query, start=start, limit=limit)
    return response


@router.delete("/messages", description="Удалить все сообщения")
async def delete_messages(
    mail_api: MailhogApi = Depends(get_mailhog_api),  # noqa: B008
) -> Response:
    await mail_api.delete_api_v1_messages()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/message/{message_id}", description="Удалить сообщение")
async def delete_message(
    message_id: str,
    mail_api: MailhogApi = Depends(get_mailhog_api),  # noqa: B008
) -> Response:
    try:
        await mail_api.delete_api_v1_message(message_id=message_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except MailNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e


@router.get("/message/{message_id}", description="Получить сообщение")
async def get_message(
    message_id: str,
    mail_api: MailhogApi = Depends(get_mailhog_api),  # noqa: B008
) -> Item:
    try:
        response = await mail_api.get_api_v1_message(message_id=message_id)
    except MailNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    return response


app.include_router(router)
