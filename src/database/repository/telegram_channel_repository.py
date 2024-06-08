from sqlalchemy import select
from puripy.decorator import component

from src.database import Driver
from src.database.entity import TelegramChannel, TelegramUser, TelegramSubscription

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

    async def find_by_telegram_user_subscriptions(self, telegram_user: TelegramUser) -> list[TelegramChannel]:
        # noinspection PyTypeChecker
        statement = (
            select(TelegramChannel)
            .join(TelegramSubscription)
            .where(TelegramSubscription.telegram_user == telegram_user)
        )
        return await self._fetch_all(statement)

    async def find_by_no_subscribers(self) -> list[TelegramChannel]:
        statement = (
            select(TelegramChannel)
            .outerjoin(TelegramSubscription)
        )
        return await self._fetch_all(statement)
