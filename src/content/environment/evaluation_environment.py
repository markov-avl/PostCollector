from abc import ABC, abstractmethod
from collections.abc import Callable

from aiogram.types import Message


def always_true(*_) -> bool:
    return True


def always_false(*_) -> bool:
    return False


class EvaluationEnvironment(ABC):

    @classmethod
    @abstractmethod
    def create_for(cls, message: Message) -> Callable:
        ...
