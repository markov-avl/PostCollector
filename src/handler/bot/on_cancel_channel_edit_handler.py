from typing import Any

from aiogram import types
from loguru import logger
from puripy.decorator import component

from src.markup.callbackdata import CancelChannelEditCallbackData
from src.service import TelegramUserService

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnCancelChannelEditHandler(BotEventHandler):

    def __init__(self, telegram_user_service: TelegramUserService):
        self._telegram_user_service = telegram_user_service

    def filters(self) -> list[Any]:
        return [CancelChannelEditCallbackData.filter()]

    def type(self) -> BotHandlerType:
        return BotHandlerType.CALLBACK_QUERY

    async def handle(self, callback_query: types.CallbackQuery, callback_data: CancelChannelEditCallbackData) -> None:
        logger.debug("CancelChannelEdit from {}", callback_query.from_user.username)

        telegram_user = await self._telegram_user_service.get_by_chat_id(callback_query.message.chat.id)
        telegram_user.editing_channel = None
        await self._telegram_user_service.update(telegram_user)

        await callback_query.message.edit_text("Редактирование канала отменено")
