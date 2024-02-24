from loguru import logger
from telethon import events

from puripy.decorator import component
from .client_event_handler import ClientEventHandler


@component
class OnHelloHandler(ClientEventHandler):

    def params(self) -> list[events.NewMessage]:
        return [events.NewMessage(pattern='(?i).*Hello')]

    async def handle(self, event: events.NewMessage.Event) -> None:
        logger.debug(f"Telegram client event: {event}")
        await event.reply("Привет!")
