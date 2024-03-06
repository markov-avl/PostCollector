from aiogram import types
from aiogram.filters import Command
from loguru import logger
from puripy.decorator import component

from src.database.enum import TelegramUserState
from src.service import TelegramUserService

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnCancelHandler(BotEventHandler):

    def __init__(self, telegram_user_service: TelegramUserService):
        self._telegram_user_service = telegram_user_service

    def params(self) -> list[Command]:
        return [Command("cancel")]

    def type(self) -> BotHandlerType:
        return BotHandlerType.MESSAGE

    async def handle(self, message: types.Message) -> None:
        logger.debug("CancelCommand from {}", message.from_user.username)

        telegram_user = await self._telegram_user_service.get_by_chat_id_or_create(message.chat.id)

        if telegram_user.state == TelegramUserState.CHANNEL_SELECTION:
            telegram_user.state = TelegramUserState.NORMAL
            await self._telegram_user_service.update(telegram_user)
            await message.answer("Выбор канала отменен")
        else:
            await message.answer("Режим выбора канала и так был отключен")
