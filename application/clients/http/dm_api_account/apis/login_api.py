# coding: utf-8

from httpx import Response

from application.clients.http.base import BaseClient
from application.clients.http.dm_api_account.models.api_models import (
    LoginCredentials,
    UserEnvelope,
)


class LoginApi(BaseClient):
    async def post_v1_account_login(
        self,
        login_credentials: LoginCredentials,  # noqa: E501
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> UserEnvelope:
        """
                Authenticate via credentials.

        Args:
                    login_credentials(LoginCredentials): ...
                    x_dm_bb_render_mode(str, optional): Requests with user defined texts that allows usage
        of BB-codes may be rendered differently by passing
        the X-Dm-Bb-Render-Mode header of one of following
        values Html, Bb, Text, SafeHtml
                    **kwargs: аргументы поддерживаемые библиотекой httpx (data, files, headers и т.п.)

        Returns:
                    UserEnvelope: ...
        """  # noqa: D205,E501
        response = await self.post_v1_account_login_with_http_info(
            login_credentials=login_credentials,  # noqa: E501
            x_dm_bb_render_mode=x_dm_bb_render_mode,
            **kwargs,
        )
        token = response.headers.get("X-Dm-Auth-Token")
        user_envelope = UserEnvelope.model_validate_json(response.text)
        user_envelope.metadata = {"token": token}
        return user_envelope

    async def post_v1_account_login_with_http_info(
        self,
        login_credentials: LoginCredentials,  # noqa: E501
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> Response:
        """
                Authenticate via credentials.

        Args:
                    login_credentials(LoginCredentials): ...
                    x_dm_bb_render_mode(str, optional): Requests with user defined texts that allows usage
        of BB-codes may be rendered differently by passing
        the X-Dm-Bb-Render-Mode header of one of following
        values Html, Bb, Text, SafeHtml
                    **kwargs: аргументы поддерживаемые библиотекой httpx (data, files, headers и т.п.)

        Returns:
                    Response: ...
        """  # noqa: D205,E501
        # process the header parameters
        headers_map = {
            "X-Dm-Bb-Render-Mode": x_dm_bb_render_mode,
        }
        headers = {k: v for k, v in headers_map.items() if v}
        headers_from_kwargs = kwargs.get("headers")
        if headers_from_kwargs:
            headers.update(headers_from_kwargs)

        response = await self.post(
            path="/v1/account/login",
            json=login_credentials.model_dump(exclude_none=True, by_alias=True),  # noqa: E501
            **kwargs,
        )
        return response

    async def delete_v1_account_login(
        self,
        x_dm_auth_token: str,
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> Response:
        """
                Logout as current user.

        Args:
                    x_dm_auth_token(str, required): Authenticated requests require X-Dm-Auth-Token
        header. You can get the data from POST /account/
        method, sending login and password in &#34;token&#34;
        response field
                    x_dm_bb_render_mode(str, optional): Requests with user defined texts that allows usage
        of BB-codes may be rendered differently by passing
        the X-Dm-Bb-Render-Mode header of one of following
        values Html, Bb, Text, SafeHtml
                    **kwargs: аргументы поддерживаемые библиотекой httpx (data, files, headers и т.п.)

        Returns:
                    None: ...
        """  # noqa: D205,E501
        response = await self.delete_v1_account_login_with_http_info(
            x_dm_auth_token=x_dm_auth_token,
            x_dm_bb_render_mode=x_dm_bb_render_mode,
            **kwargs,
        )
        return response

    async def delete_v1_account_login_with_http_info(
        self,
        x_dm_auth_token: str,
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> Response:
        """
                Logout as current user.

        Args:
                    x_dm_auth_token(str, required): Authenticated requests require X-Dm-Auth-Token
        header. You can get the data from POST /account/
        method, sending login and password in &#34;token&#34;
        response field
                    x_dm_bb_render_mode(str, optional): Requests with user defined texts that allows usage
        of BB-codes may be rendered differently by passing
        the X-Dm-Bb-Render-Mode header of one of following
        values Html, Bb, Text, SafeHtml
                    **kwargs: аргументы поддерживаемые библиотекой httpx (data, files, headers и т.п.)

        Returns:
                    Response: ...
        """  # noqa: D205,E501
        # process the header parameters
        headers_map = {
            "X-Dm-Auth-Token": x_dm_auth_token,
            "X-Dm-Bb-Render-Mode": x_dm_bb_render_mode,
        }
        headers = {k: v for k, v in headers_map.items() if v}
        headers_from_kwargs = kwargs.get("headers")
        if headers_from_kwargs:
            headers.update(headers_from_kwargs)

        response = await self.delete(
            path="/v1/account/login",
            headers=headers,
            **kwargs,
        )
        return response

    async def delete_v1_account_login_all(
        self,
        x_dm_auth_token: str,
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> Response:
        """
                Logout from every device.

        Args:
                    x_dm_auth_token(str, required): Authenticated requests require X-Dm-Auth-Token
        header. You can get the data from POST /account/
        method, sending login and password in &#34;token&#34;
        response field
                    x_dm_bb_render_mode(str, optional): Requests with user defined texts that allows usage
        of BB-codes may be rendered differently by passing
        the X-Dm-Bb-Render-Mode header of one of following
        values Html, Bb, Text, SafeHtml
                    **kwargs: аргументы поддерживаемые библиотекой httpx (data, files, headers и т.п.)

        Returns:
                    None: ...
        """  # noqa: D205,E501
        response = await self.delete_v1_account_login_all_with_http_info(
            x_dm_auth_token=x_dm_auth_token,
            x_dm_bb_render_mode=x_dm_bb_render_mode,
            **kwargs,
        )
        return response

    async def delete_v1_account_login_all_with_http_info(
        self,
        x_dm_auth_token: str,
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> Response:
        """
                Logout from every device.

        Args:
                    x_dm_auth_token(str, required): Authenticated requests require X-Dm-Auth-Token
        header. You can get the data from POST /account/
        method, sending login and password in &#34;token&#34;
        response field
                    x_dm_bb_render_mode(str, optional): Requests with user defined texts that allows usage
        of BB-codes may be rendered differently by passing
        the X-Dm-Bb-Render-Mode header of one of following
        values Html, Bb, Text, SafeHtml
                    **kwargs: аргументы поддерживаемые библиотекой httpx (data, files, headers и т.п.)

        Returns:
                    Response: ...
        """  # noqa: D205,E501
        # process the header parameters
        headers_map = {
            "X-Dm-Auth-Token": x_dm_auth_token,
            "X-Dm-Bb-Render-Mode": x_dm_bb_render_mode,
        }
        headers = {k: v for k, v in headers_map.items() if v}
        headers_from_kwargs = kwargs.get("headers")
        if headers_from_kwargs:
            headers.update(headers_from_kwargs)

        response = await self.delete(
            path="/v1/account/login/all",
            headers=headers,
            **kwargs,
        )
        return response
