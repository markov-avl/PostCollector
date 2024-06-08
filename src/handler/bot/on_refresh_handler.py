from aiogram import types
from aiogram.filters import Command
from loguru import logger
from puripy.decorator import component
from telethon.tl.custom import Dialog

from src.database.entity import TelegramChannel
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
            channel_dialog = self._find_dialog_by_channel(dialogs, channel)

            if channel_dialog is None:
                continue

            channel.name = channel_dialog.title
            await self._telegram_channel_service.update(channel)

    async def _unsubscribe_unused_channels(self) -> None:
        channels = await self._telegram_channel_service.get_all()
        unused_channels = await self._telegram_channel_service.get_by_no_subscribers()
        dialogs = list(filter(lambda d: d.is_channel, await self._telegram_client.get_dialogs()))

        for dialog in dialogs:
            channel = self._find_channel_by_dialog(channels, dialog)

            if channel is None:
                logger.debug("Unsubscribe from `{}` because of no information from DB", dialog.title)
                # await self._telegram_client.delete_dialog(dialog.id)
                continue

            if channel in unused_channels:
                logger.debug("Unsubscribe from `{}` because of no subscribers", dialog.title)
                # await self._telegram_client.delete_dialog(dialog.id)
                # await self._telegram_channel_service.delete(channel)

    @staticmethod
    def _find_dialog_by_channel(dialogs: list[Dialog], channel: TelegramChannel) -> Dialog | None:
        return next(filter(lambda d: TelegramUtility.normialize_chat_id(d.id) == channel.chat_id, dialogs), None)

    @staticmethod
    def _find_channel_by_dialog(channels: list[TelegramChannel], dialog: Dialog) -> TelegramChannel | None:
        chat_id = TelegramUtility.normialize_chat_id(dialog.id)
        return next(filter(lambda c: c.chat_id == chat_id, channels), None)
