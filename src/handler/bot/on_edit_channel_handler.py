from typing import Any

from aiogram import types
from aiogram.enums import ParseMode
from loguru import logger
from puripy.decorator import component

from src.database.entity import TelegramSubscription
from src.markup import MarkupFactory
from src.service import TelegramUserService, TelegramChannelService, TelegramSubscriptionService
from src.markup.callbackdata import EditChannelCallbackData
from src.utility import TextUtility

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnEditChannelHandler(BotEventHandler):
    MESSAGE = """
        Название канала: %s
        Правило фильтрации контента: %s
    """

    def __init__(self,
                 telegram_user_service: TelegramUserService,
                 telegram_channel_service: TelegramChannelService,
                 telegram_subscription_service: TelegramSubscriptionService):
        self._telegram_user_service = telegram_user_service
        self._telegram_channel_service = telegram_channel_service
        self._telegram_subscription_service = telegram_subscription_service

    def filters(self) -> list[Any]:
        return [EditChannelCallbackData.filter()]

    def type(self) -> BotHandlerType:
        return BotHandlerType.CALLBACK_QUERY

    async def handle(self, callback_query: types.CallbackQuery, callback_data: EditChannelCallbackData) -> None:
        logger.debug("EditChannel from {}", callback_query.from_user.username)

        telegram_user = await self._telegram_user_service.get_by_chat_id(callback_query.message.chat.id)
        telegram_channel = await self._telegram_channel_service.get_by_chat_id(callback_data.chat_id)
        telegram_subscription = await self._telegram_subscription_service \
            .get_by_telegram_user_and_telegram_channel(telegram_user, telegram_channel)

        if not telegram_subscription:
            await callback_query.message.edit_text("Невозможно отредактировать канал, так как вы уже отписаны от него")
            return

        telegram_user.editing_channel = telegram_channel
        await self._telegram_user_service.update(telegram_user)

        await callback_query.message.edit_text(
            self._get_message(telegram_subscription),
            reply_markup=MarkupFactory.edit_channel_markup(telegram_subscription),
            parse_mode=ParseMode.MARKDOWN
        )

    def _get_message(self, subscription: TelegramSubscription) -> str:
        return TextUtility.remove_indents(self.MESSAGE) % (
            subscription.telegram_channel.name,
            f"`{subscription.content_filter_query}`" if subscription.content_filter_query else "-",
        )
