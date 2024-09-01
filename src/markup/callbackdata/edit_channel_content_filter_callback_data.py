from aiogram.filters.callback_data import CallbackData


class EditChannelContentFilterCallbackData(CallbackData, prefix="editchannelcontentfilter"):
    chat_id: int
