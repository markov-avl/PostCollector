from aiogram.filters.callback_data import CallbackData


class EditChannelCallbackData(CallbackData, prefix="editchannel"):
    chat_id: int
