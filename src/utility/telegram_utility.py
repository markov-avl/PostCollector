import re
from typing import final


@final
class TelegramUtility:

    @staticmethod
    def can_be_channel_identifier(text: str) -> bool:
        return " " not in text.strip()

    @staticmethod
    def is_invite_link(link: str) -> bool:
        return TelegramUtility.parse_invite_link_hash(link) is not None

    @staticmethod
    def parse_invite_link_hash(link: str) -> str | None:
        match = re.search(r"^(https?:\/\/)?t\.me\/\+(\w+)$", link.strip())
        return match.group(2) if match else None

    @staticmethod
    def normialize_chat_id(chat_id: int) -> int:
        return int(str(chat_id)[4:]) if chat_id < 0 else chat_id
