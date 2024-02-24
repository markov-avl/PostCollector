from abc import ABC

from aiogram.filters import Command

from src.handler import EventHandler


class BotEventHandler(EventHandler, ABC):

    def params(self) -> list[Command]:
        ...
