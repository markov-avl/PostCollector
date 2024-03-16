from loguru import logger
from telethon import events
from puripy.decorator import component

from src.telegram import TelegramClient, TelegramBot
from src.service import TelegramChannelService, TelegramUserService
from src.utility import SerializationUtility

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

    def filters(self) -> list[events.NewMessage]:
        return [events.NewMessage(incoming=True, outgoing=False)]

    async def handle(self, event: events.NewMessage.Event) -> None:
        logger.debug("IncomingMessage event: {}", SerializationUtility.try_to_json(event))

        if not event.is_channel:
            return

        # It means that album was sent, it will be handled by album handler
        if event.message.grouped_id:
            return

        telegram_channel = await self._telegram_channel_service.get_by_chat_id(event.chat.id)
        if telegram_channel is None:
            return

        try:
            bot = await self._telegram_client.get_entity(self._telegram_bot.id)
        except ValueError:
            logger.error("Couldn't get bot. Maybe chat with bot is deleted or archieved")
            return

        try:
            await event.message.forward_to(bot)
        except ValueError as e:
            logger.error("Forward message error: {}", e)
