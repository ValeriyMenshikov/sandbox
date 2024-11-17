from contextlib import asynccontextmanager
from httpx import HTTPStatusError
from fastapi import HTTPException, status
import traceback


@asynccontextmanager
async def service_error_handler(status_code: int = status.HTTP_400_BAD_REQUEST):
    try:
        yield
    except HTTPStatusError as e:
        raise HTTPException(
            status_code=status_code,
            detail=e.response.json()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "details": str(e),
                "stacktrace": traceback.format_exc().split("\n"),
            },
        )
