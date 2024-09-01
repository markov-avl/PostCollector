from aiogram.filters.callback_data import CallbackData


class ReturnChannelCallbackData(CallbackData, prefix="returnchannel"):
    chat_id: int
