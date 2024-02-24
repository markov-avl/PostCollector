from abc import ABC
from typing import Any

from sqlalchemy import select
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.sql import Select

from src.database import Driver
from src.database.entity import Entity


class Repository[T: Entity](ABC):
    def __init__(self, driver: Driver, entity_type: type[Entity]):
        self._driver = driver
        self._entity_type = entity_type

    async def _execute(self, statement: Select) -> ChunkedIteratorResult:
        # noinspection PyTypeChecker
        return await self._driver.session.execute(statement)

    async def _fetch(self, statement: Select) -> T:
        result = await self._execute(statement)
        return result.scalar()

    async def _fetch_all(self, statement: Select) -> list[T]:
        result = await self._execute(statement)
        # noinspection PyTypeChecker
        return result.scalars().all()

    async def save(self, *entities: T) -> None:
        self._driver.persist(*entities)
        await self._driver.commit()

    async def remove(self, *entities: T) -> None:
        await self._driver.remove(*entities)
        await self._driver.commit()

    async def find_all(self) -> list[T]:
        statement = select(self._entity_type)
        return await self._fetch_all(statement)

    async def find_by(self, condition: Any) -> list[T]:
        statement = (
            select(self._entity_type).
            where(condition)
        )
        return await self._fetch_all(statement)

    async def find_by_id(self, id_: int) -> T:
        statement = (
            select(self._entity_type).
            where(self._entity_type.id == id_)
        )
        return await self._fetch(statement)
