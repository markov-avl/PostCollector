from puripy.decorator import property_holder


@property_holder(prefix="database")
class DatabasePropertyHolder:
    name: str
    logging: bool
