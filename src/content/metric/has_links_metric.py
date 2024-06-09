from __future__ import annotations

import re

from .content_metric import ContentMetric


class HasLinksMetric(ContentMetric):

    @classmethod
    def regex(cls) -> re.Pattern[str]:
        return re.compile(r'haslinks')

    def to_executable(self) -> str:
        return f'has_links()'

    def to_query(self) -> str:
        return f'haslinks'

    @classmethod
    def _from_match(cls, match: re.Match[str]) -> HasLinksMetric:
        return HasLinksMetric()
