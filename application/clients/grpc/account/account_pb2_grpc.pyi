"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

from abc import (
    ABCMeta,
    abstractmethod,
)
from account_pb2 import (
    ActivateAccountRequest,
    ActivateAccountResponse,
    ChangeAccountEmailRequest,
    ChangeAccountEmailResponse,
    ChangeAccountPasswordRequest,
    ChangeAccountPasswordResponse,
    GetAccountsByLoginRequest,
    GetAccountsByLoginResponse,
    GetAccountsRequest,
    GetAccountsResponse,
    GetCurrentAccountRequest,
    GetCurrentAccountResponse,
    LoginRequest,
    LoginResponse,
    LogoutAllRequest,
    LogoutRequest,
    RegisterAccountClientStreamResponse,
    RegisterAccountRequest,
    RegisterAccountResponse,
    ResetAccountPasswordRequest,
    ResetAccountPasswordResponse,
    UpdateAccountRequest,
    UpdateAccountResponse,
    User,
)
from collections.abc import (
    AsyncIterator,
    Awaitable,
    Iterator,
)
from google.protobuf.empty_pb2 import (
    Empty,
)
from grpc import (
    Channel,
    Server,
    ServicerContext,
    StreamStreamMultiCallable,
    StreamUnaryMultiCallable,
    UnaryStreamMultiCallable,
    UnaryUnaryMultiCallable,
)
from grpc.aio import (
    Channel,
    Server,
    ServicerContext,
    StreamStreamMultiCallable,
    StreamUnaryMultiCallable,
    UnaryStreamMultiCallable,
    UnaryUnaryMultiCallable,
)
from typing import (
    TypeVar,
    Union,
)

_T = TypeVar("_T")

class _MaybeAsyncIterator(AsyncIterator[_T], Iterator[_T], metaclass=ABCMeta): ...

class _ServicerContext(ServicerContext, ServicerContext):  # type: ignore[misc, type-arg]
    ...

class AccountServiceStub:
    def __init__(self, channel: Union[Channel, Channel]) -> None: ...
    Login: UnaryUnaryMultiCallable[
        LoginRequest,
        LoginResponse,
    ]

    Logout: UnaryUnaryMultiCallable[
        LogoutRequest,
        Empty,
    ]

    LogoutAll: UnaryUnaryMultiCallable[
        LogoutAllRequest,
        Empty,
    ]

    GetCurrentAccount: UnaryUnaryMultiCallable[
        GetCurrentAccountRequest,
        GetCurrentAccountResponse,
    ]

    GetAccounts: UnaryUnaryMultiCallable[
        GetAccountsRequest,
        GetAccountsResponse,
    ]

    RegisterAccount: UnaryUnaryMultiCallable[
        RegisterAccountRequest,
        RegisterAccountResponse,
    ]

    ActivateAccount: UnaryUnaryMultiCallable[
        ActivateAccountRequest,
        ActivateAccountResponse,
    ]

    ChangeAccountEmail: UnaryUnaryMultiCallable[
        ChangeAccountEmailRequest,
        ChangeAccountEmailResponse,
    ]

    ResetAccountPassword: UnaryUnaryMultiCallable[
        ResetAccountPasswordRequest,
        ResetAccountPasswordResponse,
    ]

    ChangeAccountPassword: UnaryUnaryMultiCallable[
        ChangeAccountPasswordRequest,
        ChangeAccountPasswordResponse,
    ]

    UpdateAccount: UnaryUnaryMultiCallable[
        UpdateAccountRequest,
        UpdateAccountResponse,
    ]

    RegisterAccountClientStream: StreamUnaryMultiCallable[
        RegisterAccountRequest,
        RegisterAccountClientStreamResponse,
    ]

    GetAccountsServerStream: UnaryStreamMultiCallable[
        Empty,
        User,
    ]

    GetAccountsByLoginDuplexStream: StreamStreamMultiCallable[
        GetAccountsByLoginRequest,
        GetAccountsByLoginResponse,
    ]

class AccountServiceAsyncStub:
    Login: UnaryUnaryMultiCallable[
        LoginRequest,
        LoginResponse,
    ]

    Logout: UnaryUnaryMultiCallable[
        LogoutRequest,
        Empty,
    ]

    LogoutAll: UnaryUnaryMultiCallable[
        LogoutAllRequest,
        Empty,
    ]

    GetCurrentAccount: UnaryUnaryMultiCallable[
        GetCurrentAccountRequest,
        GetCurrentAccountResponse,
    ]

    GetAccounts: UnaryUnaryMultiCallable[
        GetAccountsRequest,
        GetAccountsResponse,
    ]

    RegisterAccount: UnaryUnaryMultiCallable[
        RegisterAccountRequest,
        RegisterAccountResponse,
    ]

    ActivateAccount: UnaryUnaryMultiCallable[
        ActivateAccountRequest,
        ActivateAccountResponse,
    ]

    ChangeAccountEmail: UnaryUnaryMultiCallable[
        ChangeAccountEmailRequest,
        ChangeAccountEmailResponse,
    ]

    ResetAccountPassword: UnaryUnaryMultiCallable[
        ResetAccountPasswordRequest,
        ResetAccountPasswordResponse,
    ]

    ChangeAccountPassword: UnaryUnaryMultiCallable[
        ChangeAccountPasswordRequest,
        ChangeAccountPasswordResponse,
    ]

    UpdateAccount: UnaryUnaryMultiCallable[
        UpdateAccountRequest,
        UpdateAccountResponse,
    ]

    RegisterAccountClientStream: StreamUnaryMultiCallable[
        RegisterAccountRequest,
        RegisterAccountClientStreamResponse,
    ]

    GetAccountsServerStream: UnaryStreamMultiCallable[
        Empty,
        User,
    ]

    GetAccountsByLoginDuplexStream: StreamStreamMultiCallable[
        GetAccountsByLoginRequest,
        GetAccountsByLoginResponse,
    ]

class AccountServiceServicer(metaclass=ABCMeta):
    @abstractmethod
    def Login(
        self,
        request: LoginRequest,
        context: _ServicerContext,
    ) -> Union[LoginResponse, Awaitable[LoginResponse]]: ...

    @abstractmethod
    def Logout(
        self,
        request: LogoutRequest,
        context: _ServicerContext,
    ) -> Union[Empty, Awaitable[Empty]]: ...

    @abstractmethod
    def LogoutAll(
        self,
        request: LogoutAllRequest,
        context: _ServicerContext,
    ) -> Union[Empty, Awaitable[Empty]]: ...

    @abstractmethod
    def GetCurrentAccount(
        self,
        request: GetCurrentAccountRequest,
        context: _ServicerContext,
    ) -> Union[GetCurrentAccountResponse, Awaitable[GetCurrentAccountResponse]]: ...

    @abstractmethod
    def GetAccounts(
        self,
        request: GetAccountsRequest,
        context: _ServicerContext,
    ) -> Union[GetAccountsResponse, Awaitable[GetAccountsResponse]]: ...

    @abstractmethod
    def RegisterAccount(
        self,
        request: RegisterAccountRequest,
        context: _ServicerContext,
    ) -> Union[RegisterAccountResponse, Awaitable[RegisterAccountResponse]]: ...

    @abstractmethod
    def ActivateAccount(
        self,
        request: ActivateAccountRequest,
        context: _ServicerContext,
    ) -> Union[ActivateAccountResponse, Awaitable[ActivateAccountResponse]]: ...

    @abstractmethod
    def ChangeAccountEmail(
        self,
        request: ChangeAccountEmailRequest,
        context: _ServicerContext,
    ) -> Union[ChangeAccountEmailResponse, Awaitable[ChangeAccountEmailResponse]]: ...

    @abstractmethod
    def ResetAccountPassword(
        self,
        request: ResetAccountPasswordRequest,
        context: _ServicerContext,
    ) -> Union[ResetAccountPasswordResponse, Awaitable[ResetAccountPasswordResponse]]: ...

    @abstractmethod
    def ChangeAccountPassword(
        self,
        request: ChangeAccountPasswordRequest,
        context: _ServicerContext,
    ) -> Union[ChangeAccountPasswordResponse, Awaitable[ChangeAccountPasswordResponse]]: ...

    @abstractmethod
    def UpdateAccount(
        self,
        request: UpdateAccountRequest,
        context: _ServicerContext,
    ) -> Union[UpdateAccountResponse, Awaitable[UpdateAccountResponse]]: ...

    @abstractmethod
    def RegisterAccountClientStream(
        self,
        request_iterator: _MaybeAsyncIterator[RegisterAccountRequest],
        context: _ServicerContext,
    ) -> Union[RegisterAccountClientStreamResponse, Awaitable[RegisterAccountClientStreamResponse]]: ...

    @abstractmethod
    def GetAccountsServerStream(
        self,
        request: Empty,
        context: _ServicerContext,
    ) -> Union[Iterator[User], AsyncIterator[User]]: ...

    @abstractmethod
    def GetAccountsByLoginDuplexStream(
        self,
        request_iterator: _MaybeAsyncIterator[GetAccountsByLoginRequest],
        context: _ServicerContext,
    ) -> Union[Iterator[GetAccountsByLoginResponse], AsyncIterator[GetAccountsByLoginResponse]]: ...

def add_AccountServiceServicer_to_server(servicer: AccountServiceServicer, server: Union[Server, Server]) -> None: ...
