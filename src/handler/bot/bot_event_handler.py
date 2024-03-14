from abc import ABC, abstractmethod
from typing import Any

from src.handler import EventHandler

from .bot_handler_type import BotHandlerType


class BotEventHandler(EventHandler, ABC):

    @abstractmethod
    def filters(self) -> list[Any]:
        ...

    @abstractmethod
    def type(self) -> BotHandlerType:
        ...
