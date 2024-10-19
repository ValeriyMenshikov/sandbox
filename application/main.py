import platform

import structlog
from fastapi import FastAPI

from application import APP_MAP

# @contextlib.asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
#     interceptors = []
#     async with (
#         grpc_server(interceptors, app),
#     ):
#         yield


# app = FastAPI(lifespan=lifespan)

if platform.system() == "Linux":
    processors = [
        structlog.processors.JSONRenderer(ensure_ascii=False),
    ]
else:
    processors = [
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False),
    ]

structlog.configure(processors=processors)

main_app = FastAPI()

for app_name, app in APP_MAP.items():
    main_app.mount(f"/{app_name}", app)
