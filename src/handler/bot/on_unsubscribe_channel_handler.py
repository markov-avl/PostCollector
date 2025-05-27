from typing import Any

from aiogram import types
from loguru import logger
from puripy.decorator import component

from src.markup.callbackdata import UnsubscribeChannelCallbackData
from src.service import TelegramUserService, TelegramChannelService, TelegramSubscriptionService

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnUnsubscribeChannelHandler(BotEventHandler):

    def __init__(self,
                 telegram_user_service: TelegramUserService,
                 telegram_channel_service: TelegramChannelService,
                 telegram_subscription_service: TelegramSubscriptionService):
        self._telegram_user_service = telegram_user_service
        self._telegram_channel_service = telegram_channel_service
        self._telegram_subscription_service = telegram_subscription_service

    def filters(self) -> list[Any]:
        return [UnsubscribeChannelCallbackData.filter()]

    def type(self) -> BotHandlerType:
        return BotHandlerType.CALLBACK_QUERY

    async def handle(self, callback_query: types.CallbackQuery, callback_data: UnsubscribeChannelCallbackData) -> None:
        logger.debug("UnsubscribeChannel from {}", callback_query.from_user.username)

        telegram_user = await self._telegram_user_service.get_by_chat_id(callback_query.message.chat.id)
        telegram_channel = await self._telegram_channel_service.get_by_chat_id(callback_data.chat_id)

        if not telegram_channel:
            await callback_query.message.edit_text("Вы уже не подписаны на этот канал")
            return

        telegram_subscription = await self._telegram_subscription_service \
            .get_by_telegram_user_and_telegram_channel(telegram_user, telegram_channel)
        await self._telegram_subscription_service.delete(telegram_subscription)

        await callback_query.message.edit_text(f"Вы успешно отписались от {telegram_channel.name}")
