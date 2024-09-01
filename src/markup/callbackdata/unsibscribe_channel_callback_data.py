from aiogram.filters.callback_data import CallbackData


class UnsubscribeChannelCallbackData(CallbackData, prefix="unsubscribechannel"):
    chat_id: int
