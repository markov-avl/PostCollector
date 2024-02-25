from puripy.decorator import component
from sqlalchemy import select, and_

from src.database import Driver
from src.database.entity import TelegramSubscription, TelegramUser, TelegramChannel

from .repository import Repository


@component
class TelegramSubscriptionRepository(Repository[TelegramSubscription]):

    def __init__(self, driver: Driver):
        super().__init__(driver, TelegramSubscription)

    async def find_by_telegram_user_and_telegram_channel(self,
                                                         telegram_user: TelegramUser,
                                                         telegram_channel: TelegramChannel) \
            -> TelegramSubscription | None:
        statement = (
            select(TelegramSubscription)
            .where(and_(
                TelegramSubscription.telegram_user == telegram_user,
                TelegramSubscription.telegram_channel == telegram_channel
            ))
        )
        return await self._fetch(statement)
