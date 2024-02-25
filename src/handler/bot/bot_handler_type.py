from enum import Enum, auto


class BotHandlerType(Enum):
    MESSAGE = auto()
    CALLBACK_QUERY = auto()
