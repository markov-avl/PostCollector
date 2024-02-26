from aiogram import types
from aiogram.filters import Command, CommandStart
from loguru import logger
from puripy.decorator import component

from src.utility import TextUtility
from src.database.entity import TelegramUser
from src.service import TelegramUserService

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnStartHandler(BotEventHandler):
    MESSAGE = """
            %s!

            Я умею собирать новости из списка твоих каналов в одно место: в этот чат.

            Тебе нужно лишь сказать, какие каналы мне нужно слушать, и я буду оттуда пересылать тебе новости:
            /subscribe - подписаться на канал
            /edit - отредактировать текущие подписки
        """

    def __init__(self, telegram_user_service: TelegramUserService):
        self._telegram_user_service = telegram_user_service

    def params(self) -> list[Command]:
        return [CommandStart()]

    def type(self) -> BotHandlerType:
        return BotHandlerType.MESSAGE

    async def handle(self, message: types.Message) -> None:
        logger.debug("StartCommand from {}", message.from_user.username)

        if await self._telegram_user_service.get_by_chat_id(message.chat.id):
            answer = TextUtility.remove_indents(self.MESSAGE) % "Еще раз привет"
        else:
            telegram_user = TelegramUser()
            telegram_user.chat_id = message.chat.id
            await self._telegram_user_service.save(telegram_user)
            answer = TextUtility.remove_indents(self.MESSAGE) % "Привет"

        await message.answer(text=answer)
