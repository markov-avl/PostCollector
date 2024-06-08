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

        await self._update_channel_titles()
        await self._unsubscribe_unused_channels()

    async def _update_channel_titles(self) -> None:
        channels = await self._telegram_channel_service.get_all()
        dialogs = list(filter(lambda d: d.is_channel, await self._telegram_client.get_dialogs()))

        for channel in channels:
            channel_dialog = self._find_dialog_by_chat_id(dialogs, channel.chat_id)

            if channel_dialog is None:
                continue

            channel.name = channel_dialog.title
            await self._telegram_channel_service.update(channel)

    async def _unsubscribe_unused_channels(self) -> None:
        channels = await self._telegram_channel_service.get_by_no_subscribers()
        dialogs = list(filter(lambda d: d.is_channel, await self._telegram_client.get_dialogs()))

        for channel in channels:
            channel_dialog = self._find_dialog_by_chat_id(dialogs, channel.chat_id)

            if channel_dialog is None:
                continue

            logger.debug("Unsubscribe from `{}` because of no subscribers", channel_dialog.title)
            # await self._telegram_client.delete_dialog(channel_dialog.id)
            # await self._telegram_channel_service.delete(channel)

    @staticmethod
    def _find_dialog_by_chat_id(dialogs: list[Dialog], chat_id: int) -> Dialog | None:
        return next(filter(lambda d: TelegramUtility.normialize_chat_id(d.id) == chat_id, dialogs), None)
