from aiogram.filters.callback_data import CallbackData


class RemoveChannelCallbackData(CallbackData, prefix="removechannel"):
    channel_id: int
