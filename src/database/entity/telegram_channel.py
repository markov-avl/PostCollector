from sqlalchemy import Column, BigInteger, Boolean
from sqlalchemy.orm import Mapped

from .entity import Entity


class TelegramChannel(Entity):
    __tablename__ = "telegram_channel"

    chat_id: Mapped[int] = Column(BigInteger, unique=True, nullable=False)
    subscribed: Mapped[bool] = Column(Boolean, nullable=False, default=False)
