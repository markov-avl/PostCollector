from __future__ import annotations

import re

from .content_metric import ContentMetric


class HasVideoMetric(ContentMetric):

    @classmethod
    def regex(cls) -> re.Pattern[str]:
        return re.compile(r'hasvideo')

    def to_executable(self) -> str:
        return f'has_video()'

    def to_query(self) -> str:
        return f'hasvideo'

    @classmethod
    def _from_match(cls, match: re.Match[str]) -> HasVideoMetric:
        return HasVideoMetric()
