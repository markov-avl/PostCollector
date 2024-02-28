from puripy.decorator import component

from src.database.entity import TelegramChannel
from src.database.repository import TelegramChannelRepository


@component
class TelegramChannelService:

    def __init__(self, telegram_channel_repository: TelegramChannelRepository):
        self._telegram_channel_repository = telegram_channel_repository

    async def get_all(self) -> list[TelegramChannel]:
        return await self._telegram_channel_repository.find_all()

    async def get_by_name(self, name: str) -> TelegramChannel | None:
        return await self._telegram_channel_repository.find_by_name(name)

    async def save(self, telegram_channel: TelegramChannel) -> None:
        if await self.get_by_name(telegram_channel.name):
            raise ValueError("Telegram channel with such name is already exist")
        await self._telegram_channel_repository.save(telegram_channel)
