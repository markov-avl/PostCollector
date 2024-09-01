from aiogram.filters.callback_data import CallbackData


class AddChannelContentFilterCallbackData(CallbackData, prefix="addchannelcontentfilter"):
    chat_id: int
