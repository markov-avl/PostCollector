from __future__ import annotations

import re

from .content_criteria import ContentCriteria


class VideoCriteria(ContentCriteria):

    @classmethod
    def name(cls) -> str:
        return "video"

    @classmethod
    def regex(cls) -> re.Pattern[str]:
        return re.compile(cls.name() + r'\(\)')

    def to_evaluatable(self) -> str:
        return f"{self.name()}()"

    def to_query(self) -> str:
        return f"{self.name()}()"

    @classmethod
    def _from_match(cls, match: re.Match[str]) -> VideoCriteria:
        return VideoCriteria()
