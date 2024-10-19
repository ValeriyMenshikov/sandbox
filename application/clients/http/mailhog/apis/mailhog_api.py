from application.clients.http.base import BaseClient
from application.clients.http.mailhog.models.models import Messages


class MailhogApi(BaseClient):

    async def get_api_v2_messages(
            self,
            limit=50
    ):
        """
        Get Users emails
        :return:
        """
        params = {
            'limit': limit,
        }
        response = await self.get(
            path=f'/api/v2/messages',
            params=params,
        )
        return Messages.model_validate_json(response.content)

    async def get_api_v2_search(self, kind, query, start=0, limit=50):
        """
        Search emails
        :param kind:
        :param query:
        :param start:
        :param limit:
        :return:
        """
        params = {
            'kind': kind,
            'query': query,
            'start': start,
            'limit': limit
        }
        response = await self.get(
            path=f"/api/v2/search",
            params=params,
        )
        return Messages.model_validate_json(response.content)
