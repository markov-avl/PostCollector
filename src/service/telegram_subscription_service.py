from puripy.decorator import component

from src.database.entity import TelegramSubscription, TelegramUser, TelegramChannel
from src.database.repository import TelegramSubscriptionRepository


@component
class TelegramSubscriptionService:

    def __init__(self, telegram_subscription_repository: TelegramSubscriptionRepository):
        self._telegram_subscription_repository = telegram_subscription_repository

    async def get_all(self) -> list[TelegramSubscription]:
        return await self._telegram_subscription_repository.find_all()

    async def get_by_telegram_user_and_telegram_channel(self,
                                                        telegram_user: TelegramUser,
                                                        telegram_channel: TelegramChannel) \
            -> TelegramSubscription | None:
        return await self._telegram_subscription_repository \
            .find_by_telegram_user_and_telegram_channel(telegram_user, telegram_channel)

    async def save(self, telegram_subscription: TelegramSubscription) -> None:
        if await self.get_by_telegram_user_and_telegram_channel(
                telegram_subscription.telegram_user,
                telegram_subscription.telegram_channel
        ):
            raise ValueError("Telegram subscription with such telegram chat and telegram channel IDs is already exist")
        await self._telegram_subscription_repository.save(telegram_subscription)
