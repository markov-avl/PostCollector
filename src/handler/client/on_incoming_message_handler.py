from loguru import logger
from telethon import events

from puripy.decorator import component

from src.telegram import TelegramClient, TelegramBot
from src.service import TelegramChannelService, TelegramUserService

from .client_event_handler import ClientEventHandler


@component
class OnIncomingMessageHandler(ClientEventHandler):

    def __init__(self,
                 telegram_client: TelegramClient,
                 telegram_bot: TelegramBot,
                 telegram_user_service: TelegramUserService,
                 telegram_channel_service: TelegramChannelService):
        self._telegram_client = telegram_client
        self._telegram_bot = telegram_bot
        self._telegram_user_service = telegram_user_service
        self._telegram_channel_service = telegram_channel_service

    def params(self) -> list[events.NewMessage]:
        return [events.NewMessage(incoming=True, outgoing=False)]

    async def handle(self, event: events.NewMessage.Event) -> None:
        logger.debug(f"IncomingMessage event: {event}")

        if not event.is_channel:
            return

        telegram_channel = await self._telegram_channel_service.get_by_chat_id(event.chat.id)
        if telegram_channel is None:
            return

        try:
            await self._telegram_client.forward_messages(self._telegram_bot.id, event.message)
        except ValueError as e:
            logger.error("Forward message error", e)
