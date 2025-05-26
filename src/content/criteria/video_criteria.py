from __future__ import annotations

import re

from .content_criteria import ContentCriteria


class VideoCriteria(ContentCriteria):

    @classmethod
    def regex(cls) -> re.Pattern[str]:
        return re.compile(r'video')

    def to_executable(self) -> str:
        return 'video()'

    def to_query(self) -> str:
        return 'video'

    @classmethod
    def _from_match(cls, match: re.Match[str]) -> VideoCriteria:
        return VideoCriteria()
