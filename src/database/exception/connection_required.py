class ConnectionRequired(Exception):
    def __init__(self) -> None:
        super().__init__('This method requires database connection')
