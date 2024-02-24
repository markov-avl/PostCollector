from puripy.decorator import component
from src.database.entity import TelegramChat
from src.database.repository.telegram_chat_repository import TelegramChatRepository


@component
class TelegramChatService:

    def __init__(self, telegram_chat_repository: TelegramChatRepository):
        self._telegram_chat_repository = telegram_chat_repository

    async def get_all(self) -> list[TelegramChat]:
        return await self._telegram_chat_repository.find_all()

    async def get_by_chat_id(self, chat_id: int) -> TelegramChat | None:
        return await self._telegram_chat_repository.find_by_chat_id(chat_id)

    async def save(self, telegram_chat: TelegramChat) -> None:
        if await self.get_by_chat_id(telegram_chat.chat_id):
            raise ValueError("Telegram chat with such chat ID is already exist")
        await self._telegram_chat_repository.save(telegram_chat)
