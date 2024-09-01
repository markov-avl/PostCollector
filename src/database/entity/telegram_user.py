from sqlalchemy import Column, BigInteger, Enum
from sqlalchemy.orm import Mapped

from src.database.entity import TelegramChannel
from src.database.enum import TelegramUserState
from src.utility import EntityUtility

from .entity import Entity


class TelegramUser(Entity):
    __tablename__ = "telegram_user"

    editing_channel_id: Mapped[TelegramChannel] = Column(EntityUtility.foreign_key(TelegramChannel), nullable=True)
    chat_id: Mapped[int] = Column(BigInteger, unique=True, nullable=False)
    state: Mapped[TelegramUserState] = Column(Enum(TelegramUserState), nullable=False, default=TelegramUserState.NORMAL)

    editing_channel: Mapped[TelegramChannel] = EntityUtility.relationship(TelegramChannel)
