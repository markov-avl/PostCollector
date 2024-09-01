from typing import Any

from aiogram import types
from aiogram.enums import ParseMode
from loguru import logger
from puripy.decorator import component

from src.database.enum import TelegramUserState
from src.markup.callbackdata import AddChannelContentFilterCallbackData
from src.service import TelegramUserService, TelegramChannelService, TelegramSubscriptionService
from src.utility import TextUtility

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnAddChannelContentFilterHandler(BotEventHandler):
    INSTRUCTION = """
        Напишите правило фильтрации контента канала

        Правило представляет из себя логическое выражение, где:
        - `!` - логическое отрицание;
        - `&` - логическое И;
        - `|` - логическое ИЛИ;
        - `(` и `)` - повышение приоритета предиката.
        
        Предикаты, используемые в выражении:
        
        1. `hashashtags` - предикат от нескольких аргументов, проверяющий есть ли в посте канала соответствующие хештеги
        *Пример*: `hashashtags(реклама, рассылка)`
        
        2. `haslinks` - предикат, проверяющий есть ли в посте канала какие-либо ссылки
        *Пример*: `haslinks`
        
        Примеры выражений:
        - `hashashtags (реклама) | haslinks` - фильтруются посты, в которых есть хештег #реклама или ссылки
        - `!haslinks & !(hashashtags (полезно) | hashashtags (важно))` - фильтруются посты, в которых нет ссылок и нет хештегов #полезно или #важно
        
        Примечание: пробелы в выражении никак не учитываются
    """

    def __init__(self,
                 telegram_user_service: TelegramUserService,
                 telegram_channel_service: TelegramChannelService,
                 telegram_subscription_service: TelegramSubscriptionService):
        self._telegram_user_service = telegram_user_service
        self._telegram_channel_service = telegram_channel_service
        self._telegram_subscription_service = telegram_subscription_service

    def filters(self) -> list[Any]:
        return [AddChannelContentFilterCallbackData.filter()]

    def type(self) -> BotHandlerType:
        return BotHandlerType.CALLBACK_QUERY

    async def handle(self,
                     callback_query: types.CallbackQuery,
                     callback_data: AddChannelContentFilterCallbackData) -> None:
        logger.debug("AddChannelContentFilter from {}", callback_query.from_user.username)

        telegram_user = await self._telegram_user_service.get_by_chat_id(callback_query.message.chat.id)
        telegram_channel = await self._telegram_channel_service.get_by_chat_id(callback_data.chat_id)
        telegram_subscription = await self._telegram_subscription_service \
            .get_by_telegram_user_and_telegram_channel(telegram_user, telegram_channel)

        if not telegram_subscription:
            telegram_user.editing_channel = None
            await self._telegram_user_service.update(telegram_user)
            await callback_query.message.edit_text(
                "Невозможно добавить фильтрацию контента канала, так как вы уже отписаны от него"
            )
            return

        telegram_user.state = TelegramUserState.CHANNEL_CONTENT_FILTER_SELECTION
        telegram_user.editing_channel = telegram_channel
        await self._telegram_user_service.update(telegram_user)

        await callback_query.message.edit_text(
            TextUtility.remove_indents(self.INSTRUCTION),
            parse_mode=ParseMode.MARKDOWN
        )
