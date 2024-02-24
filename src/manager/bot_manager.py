import asyncio

from aiogram import Dispatcher
from loguru import logger

from puripy.decorator import post_init, pre_del, component
from src.telegram import TelegramBot, TelegramClient
from src.handler.bot import BotEventHandler
from src.handler.client import ClientEventHandler


@component
class BotManager:

    def __init__(self,
                 telegram_bot: TelegramBot,
                 telegram_client: TelegramClient,
                 bot_handlers: list[BotEventHandler],
                 client_handlers: list[ClientEventHandler]):
        self._dispatcher = Dispatcher()
        self._telegram_bot = telegram_bot
        self._telegram_client = telegram_client
        self._bot_handlers = bot_handlers
        self._client_handlers = client_handlers

    @post_init
    def register_handlers(self) -> None:
        for handler in self._bot_handlers:
            self._dispatcher.message(*handler.params())(handler.handle)
        for handler in self._client_handlers:
            self._telegram_client.on(*handler.params())(handler.handle)

    async def start(self) -> None:
        tasks = [
            self._dispatcher.start_polling(self._telegram_bot),
            self._telegram_client.start_polling()
        ]
        logger.info("Starting to poll")
        await asyncio.gather(*tasks)

    @pre_del
    async def stop(self) -> None:
        logger.info("Stopping to poll")
        await self._dispatcher.stop_polling()
        await self._telegram_client.stop_polling()
