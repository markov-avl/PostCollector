from sqlalchemy import select

from puripy.decorator import component
from src.database import Driver
from src.database.entity import TelegramChat
from .repository import Repository


@component
class TelegramChatRepository(Repository[TelegramChat]):

    def __init__(self, driver: Driver):
        super().__init__(driver, TelegramChat)

    async def find_by_chat_id(self, chat_id: int) -> TelegramChat | None:
        # noinspection PyTypeChecker
        statement = (
            select(TelegramChat).
            where(TelegramChat.chat_id == chat_id)
        )
        return await self._fetch(statement)
