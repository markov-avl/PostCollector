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
        
        Я умею собирать новости из твоих подписок в одно место: в этот чат.
        
        Ты можешь выбрать каналы, из которых хочешь собирать оповещения, а также изменять этот список каналов.
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

        reply_markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [types.KeyboardButton(text="Выбрать канал", request_chat=types.KeyboardButtonRequestChat(request_id=1,
                                                                                                         chat_is_channel=True))],
                [types.KeyboardButton(text="Выбранные каналы (просмотр и редактирование)")]
            ]
        )

        await message.answer(
            text=answer,
            allow_sending_without_reply=False,
            reply_markup=reply_markup
        )
