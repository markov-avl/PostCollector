from abc import abstractmethod, ABC
from typing import Any


class EventHandler(ABC):

    @abstractmethod
    def params(self) -> list[Any]:
        ...

    @abstractmethod
    def handle(self, *args, **kwargs) -> None:
        ...
