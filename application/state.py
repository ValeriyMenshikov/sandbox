import dataclasses
from typing import Optional
from application.clients.grpc.account import account_pb2_grpc


@dataclasses.dataclass
class AppState:
    account_grpc_service: Optional[account_pb2_grpc.AccountServiceStub] = None


app_state = AppState()
