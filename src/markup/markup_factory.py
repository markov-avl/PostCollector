from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.entity import TelegramChannel

from .callbackdata import (AcceptUnsubscribeCallbackData,
                           CancelUnsubscribeCallbackData,
                           RemoveChannelCallbackData,
                           ReturnChannelCallbackData)


class MarkupFactory:

    @staticmethod
    def unsubscribe_markup(subscribed_channels: list[TelegramChannel],
                           channels_to_unsubscribe: set[int]) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        for channel in subscribed_channels:
            if channel.id in channels_to_unsubscribe:
                builder.button(
                    text=f"↩️ Вернуть «{channel.name}»",
                    callback_data=ReturnChannelCallbackData(channel_id=channel.id)
                )
            else:
                builder.button(
                    text=f"🗑️ Отписаться от «{channel.name}»",
                    callback_data=RemoveChannelCallbackData(channel_id=channel.id)
                )

        builder.button(text="❌ Отменить", callback_data=CancelUnsubscribeCallbackData())
        builder.button(text="✅ Подтвердить", callback_data=AcceptUnsubscribeCallbackData())
        builder.adjust(*([1] * len(subscribed_channels)), 2)

        return builder.as_markup()

    @staticmethod
    def edit_markup(subscribed_channels: list[TelegramChannel],
                    channels_to_remove: set[int]) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        for channel in subscribed_channels:
            builder.
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

        builder.adjust(*([1] * len(subscribed_channels)), 2)

        return builder.as_markup()
