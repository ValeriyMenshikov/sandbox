import traceback
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import HTTPException, status
from httpx import HTTPStatusError


@asynccontextmanager
async def service_error_handler(status_code: int = status.HTTP_400_BAD_REQUEST) -> AsyncIterator:
    try:
        yield
    except HTTPStatusError as e:
        raise HTTPException(status_code=status_code, detail=e.response.json()) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "details": str(e),
                "stacktrace": traceback.format_exc().split("\n"),
            },
        ) from e
