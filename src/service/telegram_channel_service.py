from puripy.decorator import component

from src.database.entity import TelegramChannel, TelegramUser
from src.database.repository import TelegramChannelRepository


@component
class TelegramChannelService:

    def __init__(self, telegram_channel_repository: TelegramChannelRepository):
        self._telegram_channel_repository = telegram_channel_repository
        self._removed_subscriptions: dict[int, set[int]] = {}

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

    async def get_by_telegram_user_subscriptions(self, telegram_user: TelegramUser) -> list[TelegramChannel]:
        return await self._telegram_channel_repository.find_by_telegram_user_subscriptions(telegram_user)

    async def save(self, telegram_channel: TelegramChannel) -> None:
        if await self.get_by_chat_id(telegram_channel.chat_id):
            raise ValueError("Telegram channel with such chat ID is already exist")
        await self._telegram_channel_repository.save(telegram_channel)

    async def update(self, telegram_channel: TelegramChannel) -> None:
        await self._telegram_channel_repository.save(telegram_channel)

    def temporary_remove(self, telegram_user: TelegramUser, telegram_channel: TelegramChannel) -> None:
        if telegram_user.id not in self._removed_subscriptions:
            self._removed_subscriptions[telegram_user.id] = set()
        self._removed_subscriptions[telegram_user.id].add(telegram_channel.id)

    def temporary_return(self, telegram_user: TelegramUser, telegram_channel: TelegramChannel) -> None:
        if telegram_user.id not in self._removed_subscriptions:
            return
        self._removed_subscriptions[telegram_user.id].discard(telegram_channel.id)

    def get_temporary_removes(self, telegram_user: TelegramUser) -> set[int]:
        return self._removed_subscriptions.get(telegram_user.id, set()).copy()

    def clear_temporary_removes(self, telegram_user: TelegramUser) -> None:
        self._removed_subscriptions.pop(telegram_user.id, None)
