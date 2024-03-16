from aiogram import types
from aiogram.filters import Command
from loguru import logger
from puripy.decorator import component
from telethon.tl.custom import Dialog

from src.telegram import TelegramClient
from src.service import TelegramChannelService
from src.utility import TelegramUtility

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnRefreshHandler(BotEventHandler):

    def __init__(self, telegram_channel_service: TelegramChannelService, telegram_client: TelegramClient):
        self._telegram_channel_service = telegram_channel_service
        self._telegram_client = telegram_client

    def filters(self) -> list[Command]:
        return [Command("refresh")]

    def type(self) -> BotHandlerType:
        return BotHandlerType.MESSAGE

    async def handle(self, message: types.Message) -> None:
        logger.debug("RefreshCommand from {}", message.from_user.username)

        channels = await self._telegram_channel_service.get_all()

        async for dialog in self._telegram_client.iter_dialogs():
            dialog: Dialog
            if not dialog.is_channel:
                continue

            dialog_id = TelegramUtility.normialize_chat_id(dialog.id)
            channel = next(filter(lambda c: c.chat_id == dialog_id, channels), None)

            if channel is None:
                continue

            channel.name = dialog.title
            await self._telegram_channel_service.update(channel)
