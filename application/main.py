import contextlib
import dataclasses
from typing import AsyncGenerator, Optional
from fastapi import FastAPI, Request

import grpc
from application.clients.grpc.account import account_pb2_grpc, account_pb2
from application.grpc import grpc_server
from application.state import app_state


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    interceptors = []
    async with (
        grpc_server(interceptors, app),
    ):
        yield


app = FastAPI(lifespan=lifespan)


# @app.on_event("startup")
# async def startup():
#     channel = grpc.aio.insecure_channel("5.63.153.31:5055")
#     account_grpc_service = account_pb2_grpc.AccountServiceStub(channel)
#     app_state.account_grpc_service = account_grpc_service


@app.get("/")
async def root(request: Request):

    return await request.app.state.account_grpc_service.GetCurrentAccount(account_pb2.GetCurrentAccountRequest(token=""))
