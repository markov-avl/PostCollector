from telethon import TelegramClient as TelegramClientBase

from puripy.decorator import component
from src.propertyholder import TelegramUserPropertyHolder


@component
class TelegramClient(TelegramClientBase):

    def __init__(self, telegram_user_property_holder: TelegramUserPropertyHolder):
        super().__init__(
            telegram_user_property_holder.name,
            telegram_user_property_holder.api_id,
            telegram_user_property_holder.api_hash
        )
        self._telegram_user_property_holder = telegram_user_property_holder
        self._id: int | None = None

    @property
    def id(self) -> int | None:
        return self._id

    async def start_polling(self) -> None:
        # noinspection PyUnresolvedReferences
        await self.start(
            phone=lambda: self._telegram_user_property_holder.phone
        )
        me = await self.get_me()
        self._id = me.id
        await self.run_until_disconnected()

    async def stop_polling(self) -> None:
        await self.disconnect()
