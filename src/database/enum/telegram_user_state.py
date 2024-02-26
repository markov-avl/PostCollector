from enum import IntEnum, unique


@unique
class TelegramUserState(IntEnum):
    NORMAL = 1
    MUTED = 2
    CHANNEL_SELECTION = 3

