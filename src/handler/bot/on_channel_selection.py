from typing import Any
from aiogram import types
from loguru import logger
from puripy.decorator import component
import asyncio

from telethon.errors import UsernameInvalidError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import Channel

from src.service import TelegramUserService, TelegramChannelService, TelegramSubscriptionService
from src.database.entity import TelegramSubscription
from src.telegram import TelegramClient, TelegramBot
from src.filter import SelectChannelFilter
from src.utility import TelegramUtility
from src.database.enum import TelegramUserState

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnChannelSelection(BotEventHandler):

    def __init__(self,
                 telegram_user_service: TelegramUserService,
                 telegram_channel_service: TelegramChannelService,
                 telegram_subscription_service: TelegramSubscriptionService,
                 telegram_bot: TelegramBot,
                 telegram_client: TelegramClient,
                 select_channel_filter: SelectChannelFilter):
        self._telegram_user_service = telegram_user_service
        self._telegram_channel_service = telegram_channel_service
        self._telegram_subscription_service = telegram_subscription_service
        self._telegram_bot = telegram_bot
        self._telegram_client = telegram_client
        self._select_channel_filter = select_channel_filter

    def params(self) -> list[Any]:
        return [self._select_channel_filter]

    def type(self) -> BotHandlerType:
        return BotHandlerType.MESSAGE

    async def handle(self, message: types.Message) -> None:
        logger.info("ChannelSelection event from {}", message.from_user.username)

        if not TelegramUtility.can_be_channel_identifier(message.text):
            await message.answer("Я более чем уверен, что я не смогу найти канал по такому запросу. Попробуй снова")
            return

        try:
            channel = await self._telegram_client.get_entity(message.text)
            logger.debug(f"Found entity: {channel}")
        except (UsernameInvalidError, ValueError):
            await message.answer("Ничего не могу найти. Ты уверен в действительности введенных данных? Попробуй снова")
            return

        if not isinstance(channel, Channel):
            await message.answer("Объект, найденный по данному запросу, не является каналом. Попробуй снова")
            return

        # The user is 100% exist if this handle executed
        telegram_user = await self._telegram_user_service.get_by_chat_id(message.chat.id)
        telegram_channel = await self._telegram_channel_service.get_by_chat_id_or_create(channel.id)
        telegram_subscription = await self._telegram_subscription_service \
            .get_by_telegram_user_and_telegram_channel(telegram_user, telegram_channel)

        if telegram_subscription:
            if telegram_channel.subscribed:
                await message.answer("Ты уже подписан на этот канал")
            else:
                await message.answer("Ты уже подал заявку на подписку, нужно подождать подтверждения")
            return

        telegram_subscription = TelegramSubscription()
        telegram_subscription.telegram_user = telegram_user
        telegram_subscription.telegram_channel = telegram_channel
        await self._telegram_subscription_service.save(telegram_subscription)

        telegram_user.state = TelegramUserState.NORMAL
        await self._telegram_user_service.update(telegram_user)

        if telegram_channel.subscribed:
            await message.answer(f"Ты успешно подписался на {channel.title}!")
        else:
            # noinspection PyTypeChecker
            await self._telegram_client(JoinChannelRequest(channel))
            await message.answer("Заявка на подписку подана успешно!")
