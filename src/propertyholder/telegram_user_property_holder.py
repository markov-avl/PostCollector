from puripy.decorator import property_holder


@property_holder(prefix="telegram.user")
class TelegramUserPropertyHolder:
    name: str
    phone: str
    api_id: int
    api_hash: str
