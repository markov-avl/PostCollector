from sqlalchemy import Column, BigInteger
from sqlalchemy.orm import Mapped

from .entity import Entity


class TelegramUser(Entity):
    __tablename__ = "telegram_user"

    chat_id: Mapped[int] = Column(BigInteger, unique=True, nullable=False)
