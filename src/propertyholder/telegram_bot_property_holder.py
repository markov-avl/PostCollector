from puripy.decorator import property_holder


@property_holder(prefix="telegram.bot")
class TelegramBotPropertyHolder:
    token: str
