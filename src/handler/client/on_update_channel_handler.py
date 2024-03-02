from loguru import logger
from telethon import events

from puripy.decorator import component
from telethon.tl.types import UpdateChannel, Channel

from src.telegram import TelegramClient, TelegramBot
from src.service import TelegramChannelService, TelegramUserService

from .client_event_handler import ClientEventHandler


@component
class OnUpdateChannelHandler(ClientEventHandler):

    def __init__(self,
                 telegram_client: TelegramClient,
                 telegram_bot: TelegramBot,
                 telegram_user_service: TelegramUserService,
                 telegram_channel_service: TelegramChannelService):
        self._telegram_client = telegram_client
        self._telegram_bot = telegram_bot
        self._telegram_user_service = telegram_user_service
        self._telegram_channel_service = telegram_channel_service

    def params(self) -> list[events.Raw]:
        return [events.Raw(types=UpdateChannel)]

    async def handle(self, event: UpdateChannel) -> None:
        logger.debug(f"Telegram UpdateChannel event: {event}")

        telegram_channel = await self._telegram_channel_service.get_by_chat_id(event.channel_id)
        if telegram_channel is None:
            return

        channel: Channel = await self._telegram_client.get_entity(event.channel_id)
        logger.debug(f"Telegram channel with update: {channel}")

        if channel.left or telegram_channel.subscribed:
            return

        telegram_channel.subscribed = True
        await self._telegram_channel_service.update(telegram_channel)
        logger.info(f"Successfully subscribed to {channel.id}")

        subscribed_users = await self._telegram_user_service.get_by_subscribed_to_telegram_channel(telegram_channel)
        for user in subscribed_users:
            await self._telegram_bot.send_message(user.chat_id, f"Ты успешно подписался на {channel.title}!")
