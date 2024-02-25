from abc import abstractmethod, ABC


class EventHandler(ABC):

    @abstractmethod
    def handle(self, *args, **kwargs) -> None:
        ...
