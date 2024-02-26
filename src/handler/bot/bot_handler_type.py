from enum import IntEnum, unique


@unique
class BotHandlerType(IntEnum):
    MESSAGE = 1
    CALLBACK_QUERY = 2
