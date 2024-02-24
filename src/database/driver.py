from functools import wraps
from typing import Callable

from decohints import decohints
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from puripy.decorator import component, post_init, pre_del
from src.propertyholder import DatabasePropertyHolder
from .entity import Entity
from .exception import ConnectionRequired


@decohints
def connection_required(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self._session is None:
            raise ConnectionRequired
        return method(self, *args, **kwargs)

    return wrapper


@component
class Driver:
    def __init__(self, database_property_holder: DatabasePropertyHolder) -> None:
        self._name = database_property_holder.name
        self._logging = database_property_holder.logging

        self._engine: AsyncEngine | None = None
        self._session: AsyncSession | None = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def logging(self) -> bool:
        return self._logging

    @property
    def session(self) -> AsyncSession | None:
        return self._session

    def _get_engine(self) -> AsyncEngine:
        return create_async_engine(f'sqlite+aiosqlite:///{self._name}.db', echo=self._logging)

    def _get_session(self) -> AsyncSession:
        # noinspection PyTypeChecker
        return sessionmaker(self._engine, class_=AsyncSession, expire_on_commit=False)()

    @post_init
    async def connect(self) -> None:
        await self.close()
        self._engine = self._get_engine()
        self._session = self._get_session()
        await self.create_all()

    @pre_del
    async def close(self) -> None:
        if self._engine:
            await self._session.close()
            await self._engine.dispose()
            self._session = None
            self._engine = None

    @connection_required
    async def drop_all(self) -> None:
        async with self._engine.begin() as connection:
            # noinspection PyUnresolvedReferences
            await connection.run_sync(Entity.metadata.drop_all)

    @connection_required
    async def create_all(self) -> None:
        async with self._engine.begin() as connection:
            # noinspection PyUnresolvedReferences
            await connection.run_sync(Entity.metadata.create_all)

    @connection_required
    async def recreate_all(self) -> None:
        async with self._engine.begin() as connection:
            # noinspection PyUnresolvedReferences
            await connection.run_sync(Entity.metadata.drop_all)
            # noinspection PyUnresolvedReferences
            await connection.run_sync(Entity.metadata.create_all)

    @connection_required
    def persist(self, *entities: Entity) -> None:
        self._session.add_all(entities)

    @connection_required
    async def remove(self, *entities: Entity) -> None:
        for entity in entities:
            await self._session.delete(entity)

    @connection_required
    async def commit(self) -> None:
        await self._session.commit()
