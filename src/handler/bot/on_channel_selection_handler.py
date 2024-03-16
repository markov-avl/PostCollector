from aiogram import types
from aiogram.filters import Filter
from loguru import logger
from puripy.decorator import component

from telethon.errors import UsernameInvalidError, UserAlreadyParticipantError, InviteRequestSentError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, CheckChatInviteRequest
from telethon.tl.types import Channel, ChatInvite, ChatInviteAlready, ChatInvitePeek

from src.service import TelegramUserService, TelegramChannelService, TelegramSubscriptionService
from src.database.entity import TelegramSubscription
from src.telegram import TelegramClient, TelegramBot
from src.filter import SelectChannelFilter
from src.utility import TelegramUtility
from src.database.enum import TelegramUserState

from .bot_handler_type import BotHandlerType
from .bot_event_handler import BotEventHandler


@component
class OnChannelSelectionHandler(BotEventHandler):

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

    def filters(self) -> list[Filter]:
        return [self._select_channel_filter]

    def type(self) -> BotHandlerType:
        return BotHandlerType.MESSAGE

    async def handle(self, message: types.Message) -> None:
        logger.info("ChannelSelection event from {}", message.from_user.username)

        if not TelegramUtility.can_be_channel_identifier(message.text):
            await message.answer("Невозможно найти канал по такому запросу. Проверьте введенные данные")
            return

        if TelegramUtility.is_invite_link(message.text):
            invite_link_hash = TelegramUtility.parse_invite_link_hash(message.text)
            chat_invite = await self._telegram_client(CheckChatInviteRequest(invite_link_hash))

            if isinstance(chat_invite, ChatInvite):
                logger.debug("{} is invite to chat: {}", message.text.strip(), chat_invite)

                try:
                    await self._telegram_client(ImportChatInviteRequest(invite_link_hash))
                except UserAlreadyParticipantError:
                    logger.debug("Client is already subscribed via: {}", message.text.strip())
                except InviteRequestSentError:
                    logger.debug("Sent join request via: {}", message.text.strip())

            elif isinstance(chat_invite, ChatInviteAlready):
                logger.debug("{} is already invite to chat: {}", message.text.strip(), chat_invite)
            elif isinstance(chat_invite, ChatInvitePeek):
                logger.debug("{} is peek invite to chat: {}", message.text.strip(), chat_invite)

        try:
            channel = await self._telegram_client.get_entity(message.text)
            logger.debug("Found entity: {}", channel)
        except (UsernameInvalidError, ValueError):
            await message.answer("Невозможно найти канал по такому запросу. Попробуйте снова")
            return

        if not isinstance(channel, Channel):
            await message.answer("Объект, найденный по данному запросу, не является каналом. Попробуйте снова")
            return

        # The user is 100% exist if this handle executed
        telegram_user = await self._telegram_user_service.get_by_chat_id(message.chat.id)
        telegram_channel = await self._telegram_channel_service.get_by_chat_id_or_create(channel.id)
        telegram_subscription = await self._telegram_subscription_service \
            .get_by_telegram_user_and_telegram_channel(telegram_user, telegram_channel)

        if not channel.left and not telegram_channel.subscribed:
            telegram_channel.subscribed = True
            await self._telegram_channel_service.update(telegram_channel)

        if telegram_channel.name == "Unknown":
            telegram_channel.name = channel.title
            telegram_channel.joined_by = message.text
            await self._telegram_channel_service.update(telegram_channel)

        if telegram_subscription:
            if telegram_channel.subscribed:
                await message.answer("Подписка на этот канал уже оформлена")
            else:
                await message.answer("Подписка на этот канал уже подана, нужно дождаться подтверждения")
            return

        telegram_subscription = TelegramSubscription()
        telegram_subscription.telegram_user = telegram_user
        telegram_subscription.telegram_channel = telegram_channel
        await self._telegram_subscription_service.save(telegram_subscription)

        telegram_user.state = TelegramUserState.NORMAL
        await self._telegram_user_service.update(telegram_user)

        if telegram_channel.subscribed:
            await message.answer(f"Подписка на «{channel.title}» успешно оформлена!")
        else:
            # noinspection PyTypeChecker
            await self._telegram_client(JoinChannelRequest(channel))
            await message.answer(f"Заявка на «{channel.title}» успешно подана!")
