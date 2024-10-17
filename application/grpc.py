import contextlib
from collections import defaultdict
from typing import Optional, AsyncGenerator
from grpc_reflection.v1alpha import reflection
import grpc
from application.clients.grpc.account import account_pb2_grpc, account_pb2
from application.clients.grpc.account_proxy.account_api import AccountApiProxy


@contextlib.asynccontextmanager
async def grpc_server(
        interceptors: Optional[list[grpc.aio.ServerInterceptor]] = None,
        app=None
) -> AsyncGenerator[None, None]:
    interceptors = interceptors or list()

    server = grpc.aio.server(
        interceptors=interceptors,
        options=[
            ("grpc.http2.min_ping_interval_without_data_ms", 1000),
            ("grpc.http2.max_ping_strikes", 3),
        ],
    )
    channel = grpc.aio.insecure_channel("5.63.153.31:5055")
    app.state.account_grpc = account_pb2_grpc.AccountServiceStub(channel)

    account_service = AccountApiProxy(app.state.account_grpc)
    account_pb2_grpc.add_AccountServiceServicer_to_server(account_service, server)
    services_map: dict[str, dict[str, grpc.RpcMethodHandler]] = defaultdict(dict)

    # reflection
    service_names = list(services_map.keys())
    service_names.append(reflection.SERVICE_NAME)
    service_names.append(account_pb2.DESCRIPTOR.services_by_name["AccountService"].full_name)
    reflection.enable_server_reflection(service_names, server)
    server.add_insecure_port(f"[::]:50051")
    await server.start()
    await channel.close()

    yield

    await server.stop(None)
