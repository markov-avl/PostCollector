from typing import final


@final
class TelegramUtility:

    @staticmethod
    def can_be_channel_identifier(text: str) -> str:
        return " " not in text.strip()
