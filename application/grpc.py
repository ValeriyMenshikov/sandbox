import contextlib
from typing import AsyncGenerator, Optional

import grpc
from fastapi import FastAPI
from grpc_reflection.v1alpha import reflection

from application.clients.grpc.account import account_pb2_grpc
from application.clients.grpc.account_proxy import (
    account_proxy_pb2,
    account_proxy_pb2_grpc,
)
from application.clients.grpc.account_proxy.account_api import AccountApiProxy


@contextlib.asynccontextmanager
async def grpc_server(
    app: FastAPI,
    interceptors: Optional[list[grpc.aio.ServerInterceptor]] = None,
) -> AsyncGenerator[None, None]:
    interceptors = interceptors or list()

    server = grpc.aio.server(
        interceptors=interceptors,
        options=[
            ("grpc.http2.min_ping_interval_without_data_ms", 1000),
            ("grpc.http2.max_ping_strikes", 3),
        ],
    )
    # TODO переписать чтобы можно было инициализировать несколько сервисов
    channel = grpc.aio.insecure_channel("5.63.153.31:5055")
    app.state.account_grpc = account_pb2_grpc.AccountServiceStub(channel)

    account_service = AccountApiProxy(app.state.account_grpc)

    for (
        service_name,
        _service_descriptor,
    ) in account_proxy_pb2.DESCRIPTOR.services_by_name.items():
        add_service_function = getattr(account_proxy_pb2_grpc, f"add_{service_name}Servicer_to_server")
        add_service_function(account_service, server)

    service_names = [reflection.SERVICE_NAME]
    service_names.extend(service.full_name for service in account_proxy_pb2.DESCRIPTOR.services_by_name.values())
    reflection.enable_server_reflection(service_names, server)
    server.add_insecure_port("[::]:50051")
    await server.start()

    yield
    await channel.close()
    await server.stop(None)
