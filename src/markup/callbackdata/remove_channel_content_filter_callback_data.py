from aiogram.filters.callback_data import CallbackData


class RemoveChannelContentFilterCallbackData(CallbackData, prefix="removechannelcontentfilter"):
    chat_id: int
