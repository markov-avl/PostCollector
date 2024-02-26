from typing import Any
import asyncio
from aiogram import types, F
from loguru import logger
from puripy.decorator import component
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import InputChannel, Channel, InputPeerChannel, PeerChannel

from src.service import TelegramUserService, TelegramChannelService, TelegramSubscriptionService
from src.database.entity import TelegramUser, TelegramChannel, TelegramSubscription
from src.telegram import TelegramClient, TelegramBot

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnChannelSelection(BotEventHandler):

    def __init__(self,
                 telegram_user_service: TelegramUserService,
                 telegram_channel_service: TelegramChannelService,
                 telegram_subscription_service: TelegramSubscriptionService,
                 telegram_bot: TelegramBot,
                 telegram_client: TelegramClient):
        self._telegram_user_service = telegram_user_service
        self._telegram_channel_service = telegram_channel_service
        self._telegram_subscription_service = telegram_subscription_service
        self._telegram_bot = telegram_bot
        self._telegram_client = telegram_client

    def params(self) -> list[Any]:
        return [F.chat_shared]

    def type(self) -> BotHandlerType:
        return BotHandlerType.MESSAGE

    async def handle(self, message: types.Message) -> None:
        logger.info("ChannelSelection event from {}", message.from_user.username)

        telegram_user = await self._get_telegram_user(message.chat.id)
        telegram_channel = await self._get_telegram_channel(message.chat_shared.chat_id)

        telegram_subscription = await self._telegram_subscription_service \
            .get_by_telegram_user_and_telegram_channel(telegram_user, telegram_channel)
        if telegram_subscription:
            if telegram_channel.subscribed:
                await message.answer("Ты же подписан на этот канал")
            else:
                await message.answer("Ты уже подал заявку на подписку, нужно немного подождать")
            return

        telegram_subscription = TelegramSubscription()
        telegram_subscription.telegram_user = telegram_user
        telegram_subscription.telegram_channel = telegram_channel
        await self._telegram_subscription_service.save(telegram_subscription)

        if telegram_channel.subscribed:
            await message.answer("Ты успешно подписался на канал!")
        else:
            await message.answer("Заявка на подписку подана успешно!")

    async def _get_telegram_user(self, chat_id: int) -> TelegramUser:
        telegram_user = await self._telegram_user_service.get_by_chat_id(chat_id)

        if telegram_user is None:
            telegram_user = TelegramUser()
            telegram_user.chat_id = chat_id
            await self._telegram_user_service.save(telegram_user)

        return telegram_user

    async def _get_telegram_channel(self, chat_id: int) -> TelegramChannel:
        telegram_channel = await self._telegram_channel_service.get_by_chat_id(chat_id)

        if telegram_channel is None:
            telegram_channel = TelegramChannel()
            telegram_channel.chat_id = chat_id
            await self._telegram_channel_service.save(telegram_channel)
            peer_channel = PeerChannel(chat_id)
            channel = await self._telegram_client.get_input_entity(peer_channel)
            await self._telegram_client(JoinChannelRequest(channel))

        return telegram_channel
