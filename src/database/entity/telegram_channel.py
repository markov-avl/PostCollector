from sqlalchemy import Column, BigInteger, Boolean, String
from sqlalchemy.orm import Mapped

from .entity import Entity


class TelegramChannel(Entity):
    __tablename__ = "telegram_channel"

    chat_id: Mapped[int] = Column(BigInteger, unique=True, nullable=False)
    name: Mapped[str] = Column(String, nullable=False, default="Unknown")
    subscribed: Mapped[bool] = Column(Boolean, nullable=False, default=False)
    joined_by: Mapped[str | None] = Column(String, nullable=True)
