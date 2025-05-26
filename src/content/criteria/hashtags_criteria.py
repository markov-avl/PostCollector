from __future__ import annotations

import re

from .content_criteria import ContentCriteria


class HashtagsCriteria(ContentCriteria):

    def __init__(self, hashtags: list[str]):
        self._hashtags = hashtags

    @classmethod
    def regex(cls) -> re.Pattern[str]:
        return re.compile(r'hashtags\(([\wа-яА-ЯЁё,]+)\)')

    def to_executable(self) -> str:
        params = [f'"{h}"' for h in self._hashtags]
        return f'hashtags({', '.join(params)})'

    def to_query(self) -> str:
        return f'hashtags({', '.join(self._hashtags)})'

    @classmethod
    def _from_match(cls, match: re.Match[str]) -> HashtagsCriteria:
        return HashtagsCriteria(match.group(1).split(','))
