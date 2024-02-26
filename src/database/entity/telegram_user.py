from sqlalchemy import Column, BigInteger, Enum
from sqlalchemy.orm import Mapped

from src.database.enum import TelegramUserState

from .entity import Entity


class TelegramUser(Entity):
    __tablename__ = "telegram_user"

    chat_id: Mapped[int] = Column(BigInteger, unique=True, nullable=False)
    state: Mapped[TelegramUserState] = Column(Enum(TelegramUserState), nullable=False, default=TelegramUserState.NORMAL)
