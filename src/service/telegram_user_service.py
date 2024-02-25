from puripy.decorator import component

from src.database.entity import TelegramUser
from src.database.repository import TelegramUserRepository


@component
class TelegramUserService:

    def __init__(self, telegram_user_repository: TelegramUserRepository):
        self._telegram_user_repository = telegram_user_repository

    async def get_all(self) -> list[TelegramUser]:
        return await self._telegram_user_repository.find_all()

    async def get_by_chat_id(self, chat_id: int) -> TelegramUser | None:
        return await self._telegram_user_repository.find_by_chat_id(chat_id)

    async def save(self, telegram_user: TelegramUser) -> None:
        if await self.get_by_chat_id(telegram_user.chat_id):
            raise ValueError("Telegram chat with such chat ID is already exist")
        await self._telegram_user_repository.save(telegram_user)
