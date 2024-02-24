from abc import ABC

from src.handler import EventHandler


class ClientEventHandler(EventHandler, ABC):
    pass
