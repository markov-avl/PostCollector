from __future__ import annotations

import re

from .content_metric import ContentMetric


class HasHashtagsMetric(ContentMetric):

    def __init__(self, hashtags: list[str]):
        self._hashtags = hashtags

    @classmethod
    def regex(cls) -> re.Pattern[str]:
        return re.compile(r'hashashtags\(([\wа-яА-ЯЁё,]+)\)')

    def to_executable(self) -> str:
        params = map(lambda h: f'"{h}"', self._hashtags)
        return f'has_hashtags({', '.join(params)})'

    def to_query(self) -> str:
        return f'hashashtags({', '.join(self._hashtags)})'

    @classmethod
    def _from_match(cls, match: re.Match[str]) -> HasHashtagsMetric:
        return HasHashtagsMetric(match.group(1).split(','))
