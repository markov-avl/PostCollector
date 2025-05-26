from functools import lru_cache
from typing import Callable

from aiogram.types import Message

from .evaluation_environment import EvaluationEnvironment, always_false


def f(link: str) -> str:
    return link.rstrip("/&?")


class LinksEvaluationEnvironment(EvaluationEnvironment):

    @classmethod
    def create_for(cls, message: Message) -> Callable:
        if not message.entities:
            return always_false

        _links = {
            *[f(e.url) for e in message.entities if e.type == "text_link"],
            *[f(message.text[e.offset: e.offset + e.length]) for e in message.entities if e.type == "url"]
        }

        if not _links:
            return always_false

        @lru_cache
        def links(*args: str) -> bool:
            return all(f(a) in _links for a in args) if args else True

        return links
