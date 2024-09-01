from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.entity import TelegramChannel, TelegramSubscription

from .callbackdata import (AcceptUnsubscribeCallbackData,
                           AddChannelContentFilterCallbackData,
                           CancelChannelEditCallbackData,
                           CancelEditCallbackData,
                           CancelUnsubscribeCallbackData,
                           EditChannelCallbackData,
                           EditChannelContentFilterCallbackData,
                           RemoveChannelCallbackData,
                           RemoveChannelContentFilterCallbackData,
                           ReturnChannelCallbackData,
                           UnsubscribeChannelCallbackData)


class MarkupFactory:

    @staticmethod
    def unsubscribe_markup(subscribed_channels: list[TelegramChannel],
                           channels_to_unsubscribe: set[int]) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        for channel in subscribed_channels:
            if channel.id in channels_to_unsubscribe:
                builder.button(
                    text=f"↩️ Вернуть «{channel.name}»",
                    callback_data=ReturnChannelCallbackData(chat_id=channel.chat_id)
                )
            else:
                builder.button(
                    text=f"🗑️ Отписаться от «{channel.name}»",
                    callback_data=RemoveChannelCallbackData(chat_id=channel.chat_id)
                )

        builder.button(text="❌ Отменить", callback_data=CancelUnsubscribeCallbackData())
        builder.button(text="✅ Подтвердить", callback_data=AcceptUnsubscribeCallbackData())

        builder.adjust(*([1] * len(subscribed_channels)), 2)

        return builder.as_markup()

    @staticmethod
    def edit_markup(subscribed_channels: list[TelegramChannel]) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        for channel in subscribed_channels:
            builder.button(
                text=f"«{channel.name}»",
                callback_data=EditChannelCallbackData(chat_id=channel.chat_id)
            )

        builder.button(text="❌ Отменить", callback_data=CancelEditCallbackData())

        builder.adjust(1, repeat=True)

        return builder.as_markup()

    @staticmethod
    def edit_channel_markup(subscription: TelegramSubscription) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        if subscription.content_filter_query is None:
            builder.button(
                text="🖌 Добавить фильтр",
                callback_data=AddChannelContentFilterCallbackData(chat_id=subscription.telegram_channel.chat_id)
            )
        else:
            builder.button(
                text="✏️ Изменить фильтр",
                callback_data=EditChannelContentFilterCallbackData(chat_id=subscription.telegram_channel.chat_id)
            )
            builder.button(
                text="🧼 Удалить фильтр",
                callback_data=RemoveChannelContentFilterCallbackData(chat_id=subscription.telegram_channel.chat_id)
            )

        builder.button(
            text="🗑️ Отписаться",
            callback_data=UnsubscribeChannelCallbackData(chat_id=subscription.telegram_channel.chat_id)
        )
        builder.button(text="❌ Отменить", callback_data=CancelChannelEditCallbackData())

        builder.adjust(1, repeat=True)

        return builder.as_markup()
