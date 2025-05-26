from typing import Any

from aiogram import types
from aiogram.enums import ParseMode
from loguru import logger
from puripy.decorator import component

from src.markup.callbackdata import RemoveChannelContentFilterCallbackData
from src.service import TelegramUserService, TelegramChannelService, TelegramSubscriptionService
from .bot_event_handler import BotEventHandler
from .bot_handler_type import BotHandlerType


@component
class OnRemoveChannelContentFilterHandler(BotEventHandler):

    def __init__(self,
                 telegram_user_service: TelegramUserService,
                 telegram_channel_service: TelegramChannelService,
                 telegram_subscription_service: TelegramSubscriptionService):
        self._telegram_user_service = telegram_user_service
        self._telegram_channel_service = telegram_channel_service
        self._telegram_subscription_service = telegram_subscription_service

    def filters(self) -> list[Any]:
        return [RemoveChannelContentFilterCallbackData.filter()]

    def type(self) -> BotHandlerType:
        return BotHandlerType.CALLBACK_QUERY

    async def handle(self,
                     callback_query: types.CallbackQuery,
                     callback_data: RemoveChannelContentFilterCallbackData) -> None:
        logger.debug("RemoveChannelContentFilter from {}", callback_query.from_user.username)

        telegram_user = await self._telegram_user_service.get_by_chat_id(callback_query.message.chat.id)
        telegram_channel = await self._telegram_channel_service.get_by_chat_id(callback_data.chat_id)
        telegram_subscription = await self._telegram_subscription_service \
            .get_by_telegram_user_and_telegram_channel(telegram_user, telegram_channel)

        telegram_user.editing_channel = None
        await self._telegram_user_service.update(telegram_user)

        if not telegram_subscription:
            await callback_query.message.edit_text(
                "Невозможно удалить фильтрацию контента канала, так как вы уже отписаны от него"
            )
            return

        telegram_subscription.content_filter_query = None
        telegram_subscription.content_filter_evaluatable = None
        await self._telegram_subscription_service.update(telegram_subscription)

        await callback_query.message.edit_text(
            f"Фильтр контента для «{telegram_channel.name}» успешно удален!",
            parse_mode=ParseMode.MARKDOWN
        )
