# coding: utf-8

from httpx import Response

from application.clients.http.base import BaseClient
from application.clients.http.dm_api_account.models.api_models import (
    ChangeEmail,
    ChangePassword,
    Registration,
    ResetPassword,
    UserDetailsEnvelope,
    UserEnvelope,
)


class AccountApi(BaseClient):
    async def post_v1_account(
        self,
        registration: Registration,  # noqa: E501
        x_dm_auth_token: str = "",
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> Response:
        """
                Register new user.

        Args:
                    registration(Registration): ...
                    x_dm_auth_token(str, optional): Authenticated requests require X-Dm-Auth-Token
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
        response = await self.post_v1_account_with_http_info(
            registration=registration,  # noqa: E501
            x_dm_auth_token=x_dm_auth_token,
            x_dm_bb_render_mode=x_dm_bb_render_mode,
            **kwargs,
        )
        return response

    async def post_v1_account_with_http_info(
        self,
        registration: Registration,  # noqa: E501
        x_dm_auth_token: str = "",
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> Response:
        """
                Register new user.

        Args:
                    registration(Registration): ...
                    x_dm_auth_token(str, optional): Authenticated requests require X-Dm-Auth-Token
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

        response = await self.post(
            path="/v1/account",
            headers=headers,
            json=registration.model_dump(exclude_none=True, by_alias=True),  # noqa: E501
            **kwargs,
        )
        return response

    async def get_v1_account(
        self,
        x_dm_auth_token: str,
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> UserDetailsEnvelope:
        """
                Get current user.

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
                    UserDetailsEnvelope: ...
        """  # noqa: D205,E501
        response = await self.get_v1_account_with_http_info(
            x_dm_auth_token=x_dm_auth_token,
            x_dm_bb_render_mode=x_dm_bb_render_mode,
            **kwargs,
        )
        return UserDetailsEnvelope.model_validate_json(response.text)

    async def get_v1_account_with_http_info(
        self,
        x_dm_auth_token: str,
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> Response:
        """
                Get current user.

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

        response = await self.get(
            path="/v1/account",
            headers=headers,
            **kwargs,
        )
        return response

    async def put_v1_account_token(
        self,
        token: str,
        x_dm_auth_token: str = "",
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> UserEnvelope:
        """
                Activate registered user.

        Args:
                    token(str, required): Activation token
                    x_dm_auth_token(str, optional): Authenticated requests require X-Dm-Auth-Token
        header. You can get the data from POST /account/
        method, sending login and password in &#34;token&#34;
        response field
                    x_dm_bb_render_mode(str, optional): Requests with user defined texts that allows usage
        of BB-codes may be rendered differently by passing
        the X-Dm-Bb-Render-Mode header of one of following
        values Html, Bb, Text, SafeHtml
                    **kwargs: аргументы поддерживаемые библиотекой httpx (data, files, headers и т.п.)

        Returns:
                    UserEnvelope: ...
        """  # noqa: D205,E501
        response = await self.put_v1_account_token_with_http_info(
            token=token,
            x_dm_auth_token=x_dm_auth_token,
            x_dm_bb_render_mode=x_dm_bb_render_mode,
            **kwargs,
        )
        return UserEnvelope.model_validate_json(response.text)

    async def put_v1_account_token_with_http_info(
        self,
        token: str,
        x_dm_auth_token: str = "",
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> Response:
        """
                Activate registered user.

        Args:
                    token(str, required): Activation token
                    x_dm_auth_token(str, optional): Authenticated requests require X-Dm-Auth-Token
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

        response = await self.put(
            path=f"/v1/account/{token}",
            headers=headers,
            **kwargs,
        )
        return response

    async def post_v1_account_password(
        self,
        reset_password: ResetPassword,  # noqa: E501
        x_dm_auth_token: str = "",
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> UserEnvelope:
        """
                Reset registered user password.

        Args:
                    reset_password(ResetPassword): ...
                    x_dm_auth_token(str, optional): Authenticated requests require X-Dm-Auth-Token
        header. You can get the data from POST /account/
        method, sending login and password in &#34;token&#34;
        response field
                    x_dm_bb_render_mode(str, optional): Requests with user defined texts that allows usage
        of BB-codes may be rendered differently by passing
        the X-Dm-Bb-Render-Mode header of one of following
        values Html, Bb, Text, SafeHtml
                    **kwargs: аргументы поддерживаемые библиотекой httpx (data, files, headers и т.п.)

        Returns:
                    UserEnvelope: ...
        """  # noqa: D205,E501
        response = await self.post_v1_account_password_with_http_info(
            reset_password=reset_password,  # noqa: E501
            x_dm_auth_token=x_dm_auth_token,
            x_dm_bb_render_mode=x_dm_bb_render_mode,
            **kwargs,
        )
        return UserEnvelope.model_validate_json(response.text)

    async def post_v1_account_password_with_http_info(
        self,
        reset_password: ResetPassword,  # noqa: E501
        x_dm_auth_token: str = "",
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> Response:
        """
                Reset registered user password.

        Args:
                    reset_password(ResetPassword): ...
                    x_dm_auth_token(str, optional): Authenticated requests require X-Dm-Auth-Token
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

        response = await self.post(
            path="/v1/account/password",
            headers=headers,
            json=reset_password.model_dump(exclude_none=True, by_alias=True),  # noqa: E501
            **kwargs,
        )
        return response

    async def put_v1_account_password(
        self,
        change_password: ChangePassword,  # noqa: E501
        x_dm_auth_token: str = "",
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> UserEnvelope:
        """
                Change registered user password.

        Args:
                    change_password(ChangePassword): ...
                    x_dm_auth_token(str, optional): Authenticated requests require X-Dm-Auth-Token
        header. You can get the data from POST /account/
        method, sending login and password in &#34;token&#34;
        response field
                    x_dm_bb_render_mode(str, optional): Requests with user defined texts that allows usage
        of BB-codes may be rendered differently by passing
        the X-Dm-Bb-Render-Mode header of one of following
        values Html, Bb, Text, SafeHtml
                    **kwargs: аргументы поддерживаемые библиотекой httpx (data, files, headers и т.п.)

        Returns:
                    UserEnvelope: ...
        """  # noqa: D205,E501
        response = await self.put_v1_account_password_with_http_info(
            change_password=change_password,  # noqa: E501
            x_dm_auth_token=x_dm_auth_token,
            x_dm_bb_render_mode=x_dm_bb_render_mode,
            **kwargs,
        )
        return UserEnvelope.model_validate_json(response.text)

    async def put_v1_account_password_with_http_info(
        self,
        change_password: ChangePassword,  # noqa: E501
        x_dm_auth_token: str = "",
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> Response:
        """
                Change registered user password.

        Args:
                    change_password(ChangePassword): ...
                    x_dm_auth_token(str, optional): Authenticated requests require X-Dm-Auth-Token
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

        response = await self.put(
            path="/v1/account/password",
            headers=headers,
            json=change_password.model_dump(exclude_none=True, by_alias=True),  # noqa: E501
            **kwargs,
        )
        return response

    async def put_v1_account_email(
        self,
        change_email: ChangeEmail,  # noqa: E501
        x_dm_auth_token: str = "",
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> UserEnvelope:
        """
                Change registered user email.

        Args:
                    change_email(ChangeEmail): ...
                    x_dm_auth_token(str, optional): Authenticated requests require X-Dm-Auth-Token
        header. You can get the data from POST /account/
        method, sending login and password in &#34;token&#34;
        response field
                    x_dm_bb_render_mode(str, optional): Requests with user defined texts that allows usage
        of BB-codes may be rendered differently by passing
        the X-Dm-Bb-Render-Mode header of one of following
        values Html, Bb, Text, SafeHtml
                    **kwargs: аргументы поддерживаемые библиотекой httpx (data, files, headers и т.п.)

        Returns:
                    UserEnvelope: ...
        """  # noqa: D205,E501
        response = await self.put_v1_account_email_with_http_info(
            change_email=change_email,  # noqa: E501
            x_dm_auth_token=x_dm_auth_token,
            x_dm_bb_render_mode=x_dm_bb_render_mode,
            **kwargs,
        )
        return UserEnvelope.model_validate_json(response.text)

    async def put_v1_account_email_with_http_info(
        self,
        change_email: ChangeEmail,  # noqa: E501
        x_dm_auth_token: str = "",
        x_dm_bb_render_mode: str = "",
        **kwargs,
    ) -> Response:
        """
                Change registered user email.

        Args:
                    change_email(ChangeEmail): ...
                    x_dm_auth_token(str, optional): Authenticated requests require X-Dm-Auth-Token
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

        response = await self.put(
            path="/v1/account/email",
            headers=headers,
            json=change_email.model_dump(exclude_none=True, by_alias=True),  # noqa: E501
            **kwargs,
        )
        return response
