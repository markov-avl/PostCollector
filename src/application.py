from puripy import PuripyApplication
from .manager import BotManager


class Application(PuripyApplication):

    def __init__(self, bot_manager: BotManager):
        self._bot_manager = bot_manager

    async def run(self) -> None:
        await self._bot_manager.start()
