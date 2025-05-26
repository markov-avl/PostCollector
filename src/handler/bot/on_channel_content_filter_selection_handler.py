from aiogram import types
from aiogram.filters import Filter
from loguru import logger
from puripy.decorator import component

from src.content.filter import ContentFilterParser
from src.service import TelegramUserService, TelegramSubscriptionService
from src.filter import SelectChannelContentFilterFilter
from src.database.enum import TelegramUserState

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnChannelContentFilterSelectionHandler(BotEventHandler):

    def __init__(self,
                 telegram_user_service: TelegramUserService,
                 telegram_subscription_service: TelegramSubscriptionService,
                 select_channel_content_filter_filter: SelectChannelContentFilterFilter):
        self._telegram_user_service = telegram_user_service
        self._telegram_subscription_service = telegram_subscription_service
        self._select_channel_content_filter_filter = select_channel_content_filter_filter

    def filters(self) -> list[Filter]:
        return [self._select_channel_content_filter_filter]

    def type(self) -> BotHandlerType:
        return BotHandlerType.MESSAGE

    async def handle(self, message: types.Message) -> None:
        logger.debug("ChannelContentFilterSelection event from {}", message.from_user.username)

        try:
            content_filter = ContentFilterParser.parse(message.text)
        except SyntaxError as e:
            logger.debug("Content filter parsing error: message=<{}> error=<{}>", message.text, e)
            await message.answer("Ошибка синтаксиса выражения. Попробуйте снова")
            return

        # The user is 100% exist if this handle executed
        telegram_user = await self._telegram_user_service.get_by_chat_id(message.chat.id)
        telegram_channel = telegram_user.editing_channel
        telegram_subscription = await self._telegram_subscription_service \
            .get_by_telegram_user_and_telegram_channel(telegram_user, telegram_channel)

        telegram_subscription.content_filter_evaluatable = content_filter.to_evaluatable()
        telegram_subscription.content_filter_query = content_filter.to_query()
        await self._telegram_subscription_service.update(telegram_subscription)

        telegram_user.state = TelegramUserState.NORMAL
        telegram_user.editing_channel = None
        await self._telegram_user_service.update(telegram_user)

        await message.answer(f"Фильтр контента для «{telegram_channel.name}» успешно изменен!")
