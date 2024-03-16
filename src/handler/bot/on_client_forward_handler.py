from aiogram import types
from aiogram.filters import Filter
from loguru import logger
from puripy.decorator import component

from src.service import (TelegramUserService,
                         TelegramChannelService,
                         TelegramAlbumForwardService,
                         TelegramSubscriptionService)
from src.filter import ClientForwardFilter
from src.telegram import TelegramBot, TelegramClient
from src.utility import TelegramUtility, SerializationUtility

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnClientForwardHandler(BotEventHandler):

    def __init__(self,
                 telegram_user_service: TelegramUserService,
                 telegram_channel_service: TelegramChannelService,
                 telegram_forwarded_album_service: TelegramAlbumForwardService,
                 telegram_subscription_service: TelegramSubscriptionService,
                 telegram_bot: TelegramBot,
                 telegram_client: TelegramClient,
                 client_forward_filter: ClientForwardFilter):
        self._telegram_user_service = telegram_user_service
        self._telegram_channel_service = telegram_channel_service
        self._telegram_forwarded_album_service = telegram_forwarded_album_service
        self._telegram_subscription_service = telegram_subscription_service
        self._telegram_bot = telegram_bot
        self._telegram_client = telegram_client
        self._client_forward_filter = client_forward_filter

    def filters(self) -> list[Filter]:
        return [self._client_forward_filter]

    def type(self) -> BotHandlerType:
        return BotHandlerType.MESSAGE

    async def handle(self, message: types.Message) -> None:
        logger.debug("Client forward: {}", SerializationUtility.try_to_json(message))

        forward_chat_id = TelegramUtility.normialize_chat_id(message.forward_from_chat.id)

        telegram_channel = await self._telegram_channel_service.get_by_chat_id(forward_chat_id)
        if not telegram_channel:
            return

        if message.media_group_id:
            self._telegram_forwarded_album_service.forward(
                telegram_channel,
                message.chat.id,
                message.media_group_id,
                message.message_id
            )
            return

        subscribers = await self._telegram_user_service.get_by_subscription_to_telegram_channel(telegram_channel)
        for subscriber in subscribers:
            await self._telegram_bot.forward_message(subscriber.chat_id, message.chat.id, message.message_id)
