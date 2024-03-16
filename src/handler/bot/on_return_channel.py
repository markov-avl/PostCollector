from typing import Any

from aiogram import types
from loguru import logger
from puripy.decorator import component

from src.markup.callbackdata import ReturnChannelCallbackData
from src.markup import MarkupFactory
from src.service import TelegramUserService, TelegramChannelService

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnReturnChannel(BotEventHandler):

    def __init__(self, telegram_user_service: TelegramUserService, telegram_channel_service: TelegramChannelService):
        self._telegram_user_service = telegram_user_service
        self._telegram_channel_service = telegram_channel_service

    def filters(self) -> list[Any]:
        return [ReturnChannelCallbackData.filter()]

    def type(self) -> BotHandlerType:
        return BotHandlerType.CALLBACK_QUERY

    async def handle(self, callback_query: types.CallbackQuery, callback_data: ReturnChannelCallbackData) -> None:
        logger.debug("ReturnChannel from {}", callback_query.from_user.username)

        telegram_user = await self._telegram_user_service.get_by_chat_id(callback_query.message.chat.id)
        subscribed_channels = await self._telegram_channel_service.get_by_telegram_user_subscriptions(telegram_user)

        telegram_channel_to_return = next(filter(lambda c: c.id == callback_data.channel_id, subscribed_channels), None)
        if telegram_channel_to_return:
            self._telegram_channel_service.temporary_return(telegram_user, telegram_channel_to_return)

        channels_to_remove = self._telegram_channel_service.get_temporary_removes(telegram_user)

        await callback_query.message.edit_text(
            text="Выберите каналы, от которых хотите отписаться",
            reply_markup=MarkupFactory.edit_markup(subscribed_channels, channels_to_remove)
        )
