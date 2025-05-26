from __future__ import annotations

import re

from .content_criteria import ContentCriteria


class LinksCriteria(ContentCriteria):

    def __init__(self, links: list[str]):
        self._links = links

    @classmethod
    def name(cls) -> str:
        return "links"

    @classmethod
    def regex(cls) -> re.Pattern[str]:
        return re.compile(cls.name() + r'\((.+)\)')

    def to_evaluatable(self) -> str:
        params = [f'"{h}"' for h in self._links]
        return f'{self.name()}({', '.join(params)})'

    def to_query(self) -> str:
        return f'{self.name()}({', '.join(self._links)})'

    @classmethod
    def _from_match(cls, match: re.Match[str]) -> LinksCriteria:
        return LinksCriteria(match.group(1).split(','))
