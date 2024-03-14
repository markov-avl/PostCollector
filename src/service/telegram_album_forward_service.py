import asyncio

from loguru import logger
from puripy.decorator import component

from src.database.entity import TelegramChannel
from src.telegram import TelegramBot

from .telegram_user_service import TelegramUserService
from ..propertyholder import TelegramBotPropertyHolder


@component
class TelegramAlbumForwardService:

    def __init__(self,
                 telegram_user_service: TelegramUserService,
                 telegram_bot: TelegramBot,
                 telegram_bot_property_holder: TelegramBotPropertyHolder):
        self._telegram_user_service = telegram_user_service
        self._telegram_bot = telegram_bot
        self._album_forward_pause = telegram_bot_property_holder.album_forward_pause
        self._on_hold_forwards: dict[str, set] = {}

    def forward(self,
                from_telegram_channel: TelegramChannel,
                from_chat_id: int,
                media_group_id: str,
                message_id: int) -> None:
        if media_group_id in self._on_hold_forwards:
            self._on_hold_forwards[media_group_id].add(message_id)
            return

        self._on_hold_forwards[media_group_id] = {message_id}
        asyncio.get_event_loop().create_task(self._forward(from_telegram_channel, from_chat_id, media_group_id))

    async def _forward(self, from_telegram_channel: TelegramChannel, from_chat_id: int, media_group_id: str) -> None:
        await asyncio.sleep(self._album_forward_pause)

        subscribers = await self._telegram_user_service.get_by_subscribtion_to_telegram_channel(from_telegram_channel)
        if not subscribers:
            return

        message_ids = sorted(self._on_hold_forwards.pop(media_group_id))
        if not message_ids:
            logger.warning("No messages from media group {} found", media_group_id)

        for subscriber in subscribers:
            await self._telegram_bot.forward_messages(subscriber.chat_id, from_chat_id, message_ids)
