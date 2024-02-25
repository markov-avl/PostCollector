from abc import ABC, abstractmethod
from typing import Any

from src.handler import EventHandler


class ClientEventHandler(EventHandler, ABC):

    @abstractmethod
    def params(self) -> list[Any]:
        ...
