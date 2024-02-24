from sqlalchemy import Column, Integer
from sqlalchemy.orm import Mapped

from src.database.entity import Entity


class TelegramChat(Entity):
    __tablename__ = "telegram_chat"

    chat_id: Mapped[int] = Column(Integer, unique=True, nullable=False)
