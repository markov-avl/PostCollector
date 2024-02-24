from aiogram import types
from aiogram.filters import Command, CommandStart
from loguru import logger

from puripy.decorator import component
from src.utility import TextUtility
from .bot_event_handler import BotEventHandler
from ...database.entity import TelegramChat
from ...service import TelegramChatService


@component
class OnStartHandler(BotEventHandler):
    MESSAGE = """
        %s!
        
        Я умею собирать новости из твоих подписок в одно место: в этот чат.
        
        Тебе нужно лишь сказать, какие новости мне нужно слушать и пересылать тебе:
        /subscribe - подписаться на канал
        /unsubscribe - отписаться от канала
        /subscriptions - текущие подписки 
    """

    def __init__(self, telegram_chat_service: TelegramChatService):
        self._telegram_chat_service = telegram_chat_service

    def params(self) -> list[Command]:
        return [CommandStart()]

    async def handle(self, message: types.Message) -> None:
        logger.trace(f"StartCommand from {message.from_user.username}")
        if await self._telegram_chat_service.get_by_chat_id(message.chat.id):
            answer = TextUtility.remove_indents(self.MESSAGE) % "Еще раз привет"
        else:
            telegram_chat = TelegramChat()
            telegram_chat.chat_id = message.chat.id
            await self._telegram_chat_service.save(telegram_chat)
            answer = TextUtility.remove_indents(self.MESSAGE) % "Привет"
        await message.answer(answer)
