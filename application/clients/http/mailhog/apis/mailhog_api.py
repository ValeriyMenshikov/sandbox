import httpx

from application.clients.http.base import BaseClient
from application.clients.http.mailhog.models.models import Item, Messages
from application.services.mail.exceptions import MailNotFoundError


class MailhogApi(BaseClient):
    async def get_api_v2_messages(self, limit=50):
        params = {
            "limit": limit,
        }
        response = await self.get(
            path="/api/v2/messages",
            params=params,
        )
        return Messages.model_validate_json(response.content)

    async def get_api_v2_search(self, kind, query, start=0, limit=50):
        params = {"kind": kind, "query": query, "start": start, "limit": limit}
        response = await self.get(
            path="/api/v2/search",
            params=params,
        )
        return Messages.model_validate_json(response.content)

    async def delete_api_v1_messages(self):
        response = await self.delete(path="/api/v1/messages")
        return response

    async def get_api_v1_message(self, message_id: str):
        response = await self.get(path=f"/api/v1/messages/{message_id}")
        if response.text == "null":
            raise MailNotFoundError
        return Item.model_validate_json(response.content)

    async def delete_api_v1_message(self, message_id: str):
        try:
            response = await self.delete(path=f"/api/v1/messages/{message_id}")
        except httpx.HTTPStatusError as e:
            raise MailNotFoundError from e
        return response
