from puripy.decorator import component

from src.database.entity import TelegramChannel
from src.database.repository import TelegramChannelRepository


@component
class TelegramChannelService:

    def __init__(self, telegram_channel_repository: TelegramChannelRepository):
        self._telegram_channel_repository = telegram_channel_repository

    async def get_all(self) -> list[TelegramChannel]:
        return await self._telegram_channel_repository.find_all()

    async def get_by_chat_id(self, chat_id: int) -> TelegramChannel | None:
        return await self._telegram_channel_repository.find_by_chat_id(chat_id)

    async def get_by_chat_id_or_create(self, chat_id: int) -> TelegramChannel:
        telegram_channel = await self.get_by_chat_id(chat_id)

        if telegram_channel is None:
            telegram_channel = TelegramChannel()
            telegram_channel.chat_id = chat_id
            await self._telegram_channel_repository.save(telegram_channel)

        return telegram_channel

    async def save(self, telegram_channel: TelegramChannel) -> None:
        if await self.get_by_chat_id(telegram_channel.chat_id):
            raise ValueError("Telegram channel with such chat ID is already exist")
        await self._telegram_channel_repository.save(telegram_channel)

    async def update(self, telegram_channel: TelegramChannel) -> None:
        await self._telegram_channel_repository.save(telegram_channel)
