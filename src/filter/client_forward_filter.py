from aiogram.filters import Filter
from aiogram.types import Message
from puripy.decorator import component

from src.telegram import TelegramClient


@component
class ClientForwardFilter(Filter):

    def __init__(self, telegram_client: TelegramClient):
        self._telegram_client = telegram_client

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == self._telegram_client.id and message.forward_from_chat
