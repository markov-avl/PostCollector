from sqlalchemy import select
from puripy.decorator import component

from src.database import Driver
from src.database.entity import TelegramUser

from .repository import Repository


@component
class TelegramUserRepository(Repository[TelegramUser]):

    def __init__(self, driver: Driver):
        super().__init__(driver, TelegramUser)

    async def find_by_chat_id(self, chat_id: int) -> TelegramUser | None:
        # noinspection PyTypeChecker
        statement = (
            select(TelegramUser)
            .where(TelegramUser.chat_id == chat_id)
        )
        return await self._fetch(statement)
