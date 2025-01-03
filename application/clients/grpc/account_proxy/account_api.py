from application.clients.grpc.account.account_pb2_grpc import AccountServiceStub
from application.clients.grpc.account_proxy.account_proxy_pb2_grpc import AccountServiceProxyServicer


class AccountApiProxy(AccountServiceProxyServicer):
    def __init__(self, account: AccountServiceStub):
        self.account = account

    async def Login(self, request, context):  # noqa: N802
        return await self.account.Login(request, metadata=context.invocation_metadata())

    async def Logout(self, request, context):  # noqa: N802
        return await self.account.Logout(request)

    async def LogoutAll(self, request, context):  # noqa: N802
        return await self.account.LogoutAll(request)

    async def GetCurrentAccount(self, request, context):  # noqa: N802
        return await self.account.GetCurrentAccount(request)

    async def GetAccounts(self, request, context):  # noqa: N802
        return await self.account.GetAccounts(request)

    async def RegisterAccount(self, request, context):  # noqa: N802
        return await self.account.RegisterAccount(request)

    async def ActivateAccount(self, request, context):  # noqa: N802
        return await self.account.ActivateAccount(request)

    async def ChangeAccountEmail(self, request, context):  # noqa: N802
        return await self.account.ChangeAccountEmail(request)

    async def ResetAccountPassword(self, request, context):  # noqa: N802
        return await self.account.ResetAccountPassword(request)

    async def ChangeAccountPassword(self, request, context):  # noqa: N802
        return await self.account.ChangeAccountPassword(request)

    async def UpdateAccount(self, request, context):  # noqa: N802
        return await self.account.UpdateAccount(request)

    async def RegisterAccountClientStream(self, request_iterator, context):  # noqa: N802
        return await self.account.RegisterAccountClientStream(request_iterator)

    async def GetAccountsServerStream(self, request, context):  # noqa: N802
        async for response in self.account.GetAccountsServerStream(request):
            yield response

    async def GetAccountsByLoginDuplexStream(self, request_iterator, context):  # noqa: N802
        async for response in self.account.GetAccountsByLoginDuplexStream(request_iterator):
            yield response
