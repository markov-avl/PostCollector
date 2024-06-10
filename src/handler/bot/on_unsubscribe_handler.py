from aiogram import types
from aiogram.filters import Command
from loguru import logger
from puripy.decorator import component

from src.markup import MarkupFactory
from src.service import TelegramUserService, TelegramChannelService

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnUnsubscribeHandler(BotEventHandler):

    def __init__(self, telegram_user_service: TelegramUserService, telegram_channel_service: TelegramChannelService):
        self._telegram_user_service = telegram_user_service
        self._telegram_channel_service = telegram_channel_service

    def filters(self) -> list[Command]:
        return [Command("unsubscribe")]

    def type(self) -> BotHandlerType:
        return BotHandlerType.MESSAGE

    async def handle(self, message: types.Message) -> None:
        logger.debug("UnsubscribeCommand from {}", message.from_user.username)

        telegram_user = await self._telegram_user_service.get_by_chat_id_or_create(message.chat.id)
        subscribed_channels = await self._telegram_channel_service.get_by_telegram_user_subscriptions(telegram_user)

        if not subscribed_channels:
            await message.answer("У вас нет подписок, поэтому не от чего отписываться")
            return

        await message.answer(
            "Выберите каналы, от которых хотите отписаться",
            reply_markup=MarkupFactory.unsubscribe_markup(subscribed_channels, set())
        )
