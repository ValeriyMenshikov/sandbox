from typing import (
    AsyncGenerator,
    Callable,
    Type,
)

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from application.data_access.pg.base_repositoty import BaseRepository
from application.settings import Settings

engine = create_async_engine(url=Settings().db_url, future=True, echo=True, pool_pre_ping=True)

AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, autoflush=False)


async def get_connection() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session


def get_repository(
    repo_type: Type[BaseRepository],
) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repo(session: AsyncSession = Depends(get_connection)) -> BaseRepository:  # noqa: B008
        return repo_type(session)

    return _get_repo
