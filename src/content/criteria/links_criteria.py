from __future__ import annotations

import re

from .content_criteria import ContentCriteria


class LinksCriteria(ContentCriteria):

    @classmethod
    def regex(cls) -> re.Pattern[str]:
        return re.compile(r'links')

    def to_executable(self) -> str:
        return 'links()'

    def to_query(self) -> str:
        return 'links'

    @classmethod
    def _from_match(cls, match: re.Match[str]) -> LinksCriteria:
        return LinksCriteria()
