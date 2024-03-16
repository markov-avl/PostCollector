from aiogram import types
from aiogram.filters import Command
from loguru import logger
from puripy.decorator import component

from src.service import TelegramUserService
from src.database.enum import TelegramUserState

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnSubscribeHandler(BotEventHandler):

    def __init__(self, telegram_user_service: TelegramUserService):
        self._telegram_user_service = telegram_user_service

    def filters(self) -> list[Command]:
        return [Command("subscribe")]

    def type(self) -> BotHandlerType:
        return BotHandlerType.MESSAGE

    async def handle(self, message: types.Message) -> None:
        logger.debug("SubscribeCommand from {}", message.from_user.username)

        telegram_user = await self._telegram_user_service.get_by_chat_id_or_create(message.chat.id)
        telegram_user.state = TelegramUserState.CHANNEL_SELECTION
        await self._telegram_user_service.update(telegram_user)

        await message.answer("Отправьте ссылку, приглашение или @channelname канала, на который нужно подписаться")
