from aiogram import Bot as TelegramBotBase

from puripy.decorator import component
from src.propertyholder import TelegramBotPropertyHolder


@component
class TelegramBot(TelegramBotBase):

    def __init__(self, telegram_bot_property_holder: TelegramBotPropertyHolder):
        super().__init__(telegram_bot_property_holder.token)
        self._telegram_bot_property_holder = telegram_bot_property_holder
