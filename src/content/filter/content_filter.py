from src.content.metric import ContentMetric


class ContentFilter:

    def __init__(self, pattern: str, metrics: list[ContentMetric]):
        self._pattern = pattern
        self._metrics = metrics

    def to_executable(self) -> str:
        executable = self._pattern
        for metric in self._metrics:
            executable = executable.replace('?', metric.to_executable(), 1)

        return executable \
            .replace('!', 'not ') \
            .replace('|', ' or ') \
            .replace('&', ' and ')

    def to_query(self) -> str:
        query = self._pattern
        for metric in self._metrics:
            query = query.replace('?', metric.to_query(), 1)

        return query \
            .replace('|', ' | ') \
            .replace('&', ' & ')
