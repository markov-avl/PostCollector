from __future__ import annotations

import re

from .content_criteria import ContentCriteria


class HashtagsCriteria(ContentCriteria):

    def __init__(self, hashtags: list[str]):
        self._hashtags = hashtags

    @classmethod
    def name(cls) -> str:
        return "hashtags"

    @classmethod
    def regex(cls) -> re.Pattern[str]:
        return re.compile(cls.name() + r'\(([\wа-яА-ЯЁё,]+)\)')

    def to_evaluatable(self) -> str:
        params = [f'"{h}"' for h in self._hashtags]
        return f"{self.name()}({', '.join(params)})"

    def to_query(self) -> str:
        return f"{self.name()}({', '.join(self._hashtags)})"

    @classmethod
    def _from_match(cls, match: re.Match[str]) -> HashtagsCriteria:
        return HashtagsCriteria(match.group(1).split(','))
