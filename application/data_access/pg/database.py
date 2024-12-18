from typing import (
    Any,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
)


class Base(DeclarativeBase):
    id: Any
    __name__: str  # type: ignore[misc]

    __allow_unmapped__ = True

    @declared_attr  # type: ignore[arg-type]
    def __tablename__(self) -> str:
        """Generate table name from class name."""
        return self.__name__.lower()
