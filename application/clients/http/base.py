import uuid
from json.decoder import JSONDecodeError

import structlog
from curlify2 import Curlify
from httpx import (
    AsyncClient,
)


class Configuration:
    def __init__(self, host: str, headers: dict = None, disable_log: bool = True):
        self.host = host
        self.headers = headers
        self.disable_log = disable_log


class BaseClient:
    def __init__(self, configuration: Configuration):
        self.host = configuration.host
        self.set_headers(configuration.headers)
        self.disable_log = configuration.disable_log
        self.session = AsyncClient(base_url=self.host)
        self.log = structlog.get_logger(__name__).bind(service="api")

    def set_headers(self, headers):
        if headers:
            self.session.headers.update(headers)

    async def post(self, path, **kwargs):
        return await self._send_request(method="POST", path=path, **kwargs)

    async def get(self, path, **kwargs):
        return await self._send_request(method="GET", path=path, **kwargs)

    async def put(self, path, **kwargs):
        return await self._send_request(method="PUT", path=path, **kwargs)

    async def delete(self, path, **kwargs):
        return await self._send_request(method="DELETE", path=path, **kwargs)

    async def _send_request(self, method, path, **kwargs):
        log = self.log.bind(event_id=str(uuid.uuid4()))

        if self.disable_log:
            rest_response = await self.session.request(method=method, url=path, **kwargs)
            rest_response.raise_for_status()
            return rest_response

        log.msg(
            event="Request",
            method=method,
            host=self.host,
            params=kwargs.get("params"),
            headers=kwargs.get("headers"),
            json=kwargs.get("json"),
            data=kwargs.get("data"),
        )
        rest_response = await self.session.request(method=method, url=path, **kwargs)

        curl = Curlify(rest_response.request).to_curl()
        print(curl)
        log.msg(
            event="Response",
            status_code=rest_response.status_code,
            headers=rest_response.headers,
            json=self._get_json(rest_response),
        )
        rest_response.raise_for_status()
        return rest_response

    @staticmethod
    def _get_json(rest_response):
        try:
            return rest_response.json()
        except JSONDecodeError:
            return {}
