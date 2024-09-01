from typing import Any

from aiogram import types
from loguru import logger
from puripy.decorator import component

from src.markup.callbackdata import CancelEditCallbackData

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnCancelEditHandler(BotEventHandler):

    def filters(self) -> list[Any]:
        return [CancelEditCallbackData.filter()]

    def type(self) -> BotHandlerType:
        return BotHandlerType.CALLBACK_QUERY

    async def handle(self, callback_query: types.CallbackQuery, callback_data: CancelEditCallbackData) -> None:
        logger.debug("CancelEdit from {}", callback_query.from_user.username)

        await callback_query.message.edit_text("Редактирование каналов отменено")
