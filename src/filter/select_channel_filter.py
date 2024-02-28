from aiogram.filters import Filter
from aiogram.types import Message
from puripy.decorator import component

from src.database.enum import TelegramUserState
from src.service import TelegramUserService


@component
class SelectChannelFilter(Filter):

    def __init__(self, telegram_user_service: TelegramUserService):
        self._telegram_user_service = telegram_user_service

    async def __call__(self, message: Message) -> bool:
        if next(filter(lambda e: e.type == "bot_command", message.entities or []), None):
            return False

        telegram_user = await self._telegram_user_service.get_by_chat_id(message.chat.id)
        if telegram_user is None:
            return False

        return telegram_user.state == TelegramUserState.CHANNEL_SELECTION
