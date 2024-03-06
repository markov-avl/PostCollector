from aiogram import types, F
from aiogram.filters import Command
from loguru import logger
from puripy.decorator import component

from src.database.enum import TelegramUserState
from src.service import TelegramUserService, TelegramChannelService, TelegramSubscriptionService
from src.telegram import TelegramBot, TelegramClient

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnClientForwardHandler(BotEventHandler):

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

    def params(self) -> list[Command]:
        return [F.forward_from.id == 1]

    def type(self) -> BotHandlerType:
        return BotHandlerType.MESSAGE

    async def handle(self, message: types.Message) -> None:
        logger.debug("CancelCommand from {}", message.from_user.username)

        telegram_user = await self._telegram_user_service.get_by_chat_id_or_create(message.chat.id)

        if telegram_user.state == TelegramUserState.CHANNEL_SELECTION:
            telegram_user.state = TelegramUserState.NORMAL
            await self._telegram_user_service.update(telegram_user)
            await message.answer("Выбор канала отменен")
        else:
            await message.answer("Ты и так не был в режиме выбора канала")
