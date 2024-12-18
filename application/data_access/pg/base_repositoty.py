from typing import Any

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from sqlalchemy.sql.base import Executable


class BaseRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def execute(self, query: Executable, autocommit: bool = True) -> Result[Any]:
        async with self.db_session as session:
            result = await session.execute(query)
            if autocommit:
                await session.commit()
            return result
