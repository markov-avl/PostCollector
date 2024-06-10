from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped

from src.utility import EntityUtility

from .telegram_user import TelegramUser
from .telegram_channel import TelegramChannel
from .entity import Entity


class TelegramSubscription(Entity):
    __tablename__ = "telegram_subscription"

    telegram_user_id: Mapped[int] = Column(EntityUtility.foreign_key(TelegramUser), nullable=False)
    telegram_channel_id: Mapped[int] = Column(EntityUtility.foreign_key(TelegramChannel), nullable=False)
    # content_filter_executable: Mapped[str] = Column(String, nullable=True, default=None)
    # content_filter_query: Mapped[str] = Column(String, nullable=True, default=None)

    telegram_user: Mapped[TelegramUser] = EntityUtility.relationship(TelegramUser)
    telegram_channel: Mapped[TelegramChannel] = EntityUtility.relationship(TelegramChannel)
