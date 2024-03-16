from typing import Any

from aiogram import types
from loguru import logger
from puripy.decorator import component

from src.markup.callbackdata import CancelEditCallbackData
from src.service import TelegramUserService, TelegramChannelService

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnCancelEdit(BotEventHandler):

    def __init__(self, telegram_user_service: TelegramUserService, telegram_channel_service: TelegramChannelService):
        self._telegram_user_service = telegram_user_service
        self._telegram_channel_service = telegram_channel_service

    def filters(self) -> list[Any]:
        return [CancelEditCallbackData.filter()]

    def type(self) -> BotHandlerType:
        return BotHandlerType.CALLBACK_QUERY

    async def handle(self, callback_query: types.CallbackQuery, callback_data: CancelEditCallbackData) -> None:
        logger.debug("CancelEdit from {}", callback_query.from_user.username)

        telegram_user = await self._telegram_user_service.get_by_chat_id(callback_query.message.chat.id)
        self._telegram_channel_service.clear_temporary_removes(telegram_user)

        await callback_query.message.edit_text(text="Редактирование каналов отменено")
