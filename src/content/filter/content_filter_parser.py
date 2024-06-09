from .content_filter import ContentFilter

from src.content.metric import ContentMetric, HasHashtagsMetric, HasLinksMetric, HasVideoMetric


class ContentFilterParser:

    @classmethod
    def parse(cls, query: str) -> ContentFilter:
        content_metrics = cls.parse_content_metrics(query)

        pattern = query.replace(' ', '')
        for _, match, _ in content_metrics:
            pattern = pattern.replace(match, '?', 1)

        cls.check_query_pattern(pattern)

        return ContentFilter(pattern, [cm for _, _, cm in content_metrics])

    @classmethod
    def parse_content_metrics(cls, query: str) -> list[ContentMetric]:
        return sorted([
            *HasHashtagsMetric.find(query),
            *HasLinksMetric.find(query),
            *HasVideoMetric.find(query)
        ], key=lambda cm: cm[0])

    @classmethod
    def check_query_pattern(cls, pattern: str) -> None:
        code = pattern \
            .replace('!', ' not ') \
            .replace('|', ' or ') \
            .replace('&', ' and ') \
            .replace('?', 'True')
        try:
            eval(code)
        except SyntaxError:
            raise SyntaxError('Invalid query syntax')
