from .content_filter import ContentFilter

from src.content.criteria import ContentCriteria, HashtagsCriteria, LinksCriteria, VideoCriteria


class ContentFilterParser:
    CRITERIA = {HashtagsCriteria, LinksCriteria, VideoCriteria}

    @classmethod
    def parse(cls, query: str) -> ContentFilter:
        content_criteria = cls.parse_content_criteria(query)

        pattern = query.replace(' ', '')
        for _, match, _ in content_criteria:
            pattern = pattern.replace(match, '?', 1)

        cls.validate_query_pattern(pattern)

        return ContentFilter(pattern, [cc for _, _, cc in content_criteria])

    @classmethod
    def parse_content_criteria(cls, query: str) -> list[tuple[int, str, ContentCriteria]]:
        return sorted([
            *HashtagsCriteria.find(query),
            *LinksCriteria.find(query),
            *VideoCriteria.find(query)
        ], key=lambda cm: cm[0])

    @classmethod
    def validate_query_pattern(cls, pattern: str) -> None:
        code = pattern \
            .replace('!', ' not ') \
            .replace('|', ' or ') \
            .replace('&', ' and ') \
            .replace('?', 'True')
        try:
            eval(code)
        except SyntaxError:
            raise SyntaxError('Invalid query syntax')
