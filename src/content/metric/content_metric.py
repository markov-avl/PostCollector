from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Iterator


class ContentMetric(ABC):

    @classmethod
    @abstractmethod
    def regex(cls) -> re.Pattern[str]:
        ...

    @abstractmethod
    def to_executable(self) -> str:
        ...

    @abstractmethod
    def to_query(self) -> str:
        ...

    @classmethod
    def find(cls, query: str) -> Iterator[tuple[int, str, ContentMetric]]:
        for match in cls._find_iter(query):
            metric = cls._from_match(match)
            yield cls._with_match_info(match, metric)

    @classmethod
    @abstractmethod
    def _from_match(cls, match: re.Match[str]) -> ContentMetric:
        ...

    @classmethod
    def _find_iter(cls, query: str) -> Iterator[re.Match[str]]:
        return re.finditer(cls.regex(), query.replace(' ', ''))

    @classmethod
    def _with_match_info(cls, match: re.Match[str], content_metric: ContentMetric) -> tuple[int, str, ContentMetric]:
        return match.span(0)[0], match.group(0), content_metric

    def __repr__(self):
        return self.to_executable()
