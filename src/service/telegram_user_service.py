from puripy.decorator import component

from src.database.entity import TelegramUser, TelegramChannel
from src.database.repository import TelegramUserRepository


@component
class TelegramUserService:

    def __init__(self, telegram_user_repository: TelegramUserRepository):
        self._telegram_user_repository = telegram_user_repository

    async def get_all(self) -> list[TelegramUser]:
        return await self._telegram_user_repository.find_all()

    async def get_by_chat_id(self, chat_id: int) -> TelegramUser | None:
        return await self._telegram_user_repository.find_by_chat_id(chat_id)

    async def get_by_chat_id_or_create(self, chat_id: int) -> TelegramUser:
        telegram_user = await self.get_by_chat_id(chat_id)

        if telegram_user is None:
            telegram_user = TelegramUser()
            telegram_user.chat_id = chat_id
            await self._telegram_user_repository.save(telegram_user)

        return telegram_user

    async def get_by_subscribed_to_telegram_channel(self, telegram_channel: TelegramChannel) -> list[TelegramUser]:
        return await self._telegram_user_repository.find_by_subscribed_to_telegram_channel(telegram_channel)

    async def save(self, telegram_user: TelegramUser) -> None:
        if await self.get_by_chat_id(telegram_user.chat_id):
            raise ValueError("Telegram chat with such chat ID is already exist")
        await self._telegram_user_repository.save(telegram_user)

    async def update(self, telegram_user: TelegramUser) -> None:
        await self._telegram_user_repository.save(telegram_user)
