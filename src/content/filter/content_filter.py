from src.content.criteria import ContentCriteria


class ContentFilter:

    def __init__(self, pattern: str, criteria: list[ContentCriteria]):
        self._pattern = pattern
        self._criteria = criteria

    def to_evaluatable(self) -> str:
        evaluatable = self._pattern
        for criteria in self._criteria:
            evaluatable = evaluatable.replace('?', criteria.to_evaluatable(), 1)

        return evaluatable \
            .replace('!', 'not ') \
            .replace('|', ' or ') \
            .replace('&', ' and ')

    def to_query(self) -> str:
        query = self._pattern
        for criteria in self._criteria:
            query = query.replace('?', criteria.to_query(), 1)

        return query \
            .replace('|', ' | ') \
            .replace('&', ' & ')
