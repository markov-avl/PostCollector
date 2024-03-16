from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.entity import TelegramChannel

from .callbackdata import (AcceptEditCallbackData,
                           CancelEditCallbackData,
                           RemoveChannelCallbackData,
                           ReturnChannelCallbackData)


class MarkupFactory:

    @staticmethod
    def edit_markup(subscribed_channels: list[TelegramChannel], channels_to_remove: set[int]) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        for channel in subscribed_channels:
            if channel.id in channels_to_remove:
                builder.button(
                    text=f"↩️ Вернуть «{channel.name}»",
                    callback_data=ReturnChannelCallbackData(channel_id=channel.id)
                )
            else:
                builder.button(
                    text=f"🗑️ Отписаться от «{channel.name}»",
                    callback_data=RemoveChannelCallbackData(channel_id=channel.id)
                )

        builder.button(text="❌ Отменить", callback_data=CancelEditCallbackData())
        builder.button(text="✅ Подтвердить", callback_data=AcceptEditCallbackData())
        builder.adjust(*([1] * len(subscribed_channels)), 2)

        return builder.as_markup()
