from sqlalchemy import select
from puripy.decorator import component

from src.database import Driver
from src.database.entity import TelegramChannel

from .repository import Repository


@component
class TelegramChannelRepository(Repository[TelegramChannel]):

    def __init__(self, driver: Driver):
        super().__init__(driver, TelegramChannel)

    async def find_by_chat_id(self, chat_id: int) -> TelegramChannel | None:
        # noinspection PyTypeChecker
        statement = (
            select(TelegramChannel)
            .where(TelegramChannel.chat_id == chat_id)
        )
        return await self._fetch(statement)