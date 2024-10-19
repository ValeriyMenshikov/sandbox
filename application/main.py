import contextlib
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from starlette.applications import Starlette

from application import APP_MAP
from application.clients.grpc.account import account_pb2
from application.grpc import grpc_server

# @contextlib.asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
#     interceptors = []
#     async with (
#         grpc_server(interceptors, app),
#     ):
#         yield


# app = FastAPI(lifespan=lifespan)

from fastapi import FastAPI

main_app = FastAPI()

for app_name, app in APP_MAP.items():
    main_app.mount(f"/{app_name}", app)
