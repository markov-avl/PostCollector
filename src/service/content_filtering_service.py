from aiogram.types import Message
from puripy.decorator import component

from src.database.entity import TelegramChannel, TelegramUser, TelegramSubscription
from src.content.criteria import LinksCriteria
from src.content.environment import LinksEvaluationEnvironment

from .telegram_subscription_service import TelegramSubscriptionService


@component
class ContentFilteringService:

    def __init__(self, telegram_subscription_service: TelegramSubscriptionService):
        self._telegram_subscription_service = telegram_subscription_service

    async def filter_subscribers(self, message: Message, telegram_channel: TelegramChannel) -> list[TelegramUser]:
        subscriptions = await self._telegram_subscription_service.get_by_telegram_channel(telegram_channel)
        return [s.telegram_user for s in self._filtered(message, subscriptions)]

    @staticmethod
    def _filtered(message: Message, subscriptions: list[TelegramSubscription]) -> list[TelegramSubscription]:
        return [s for s in subscriptions if not s.content_filter_evaluatable or eval(s.content_filter_evaluatable, {
            LinksCriteria.name(): LinksEvaluationEnvironment.create_for(message)
        })]
