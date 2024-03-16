from typing import Any

from aiogram import types
from loguru import logger
from puripy.decorator import component

from src.markup.callbackdata import AcceptEditCallbackData
from src.service import TelegramUserService, TelegramChannelService, TelegramSubscriptionService

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnAcceptEdit(BotEventHandler):

    def __init__(self,
                 telegram_user_service: TelegramUserService,
                 telegram_channel_service: TelegramChannelService,
                 telegram_subscription_service: TelegramSubscriptionService):
        self._telegram_user_service = telegram_user_service
        self._telegram_channel_service = telegram_channel_service
        self._telegram_subscription_service = telegram_subscription_service

    def filters(self) -> list[Any]:
        return [AcceptEditCallbackData.filter()]

    def type(self) -> BotHandlerType:
        return BotHandlerType.CALLBACK_QUERY

    async def handle(self, callback_query: types.CallbackQuery, callback_data: AcceptEditCallbackData) -> None:
        logger.debug("AcceptEdit from {}", callback_query.from_user.username)

        telegram_user = await self._telegram_user_service.get_by_chat_id(callback_query.message.chat.id)
        channels_to_remove = self._telegram_channel_service.get_temporary_removes(telegram_user)

        if not channels_to_remove:
            await callback_query.message.edit_text(text="Ни один канал не был выбран")
            return

        subscribed_channels = await self._telegram_channel_service.get_by_telegram_user_subscriptions(telegram_user)
        unsubscribed_channels = []

        for channel in subscribed_channels:
            if channel.id in channels_to_remove:
                telegram_subscription = await self._telegram_subscription_service \
                    .get_by_telegram_user_and_telegram_channel(telegram_user, channel)
                await self._telegram_subscription_service.delete(telegram_subscription)
                unsubscribed_channels.append(channel)

        unsubscribed_channel_names = ', '.join(f'«{channel.name}»' for channel in unsubscribed_channels)

        if unsubscribed_channel_names:
            await callback_query.message.edit_text(text=f"Вы успешно отписались от {unsubscribed_channel_names}")
        else:
            await callback_query.message.edit_text(text="Вы и так не были подписаны на выбранные каналы")
