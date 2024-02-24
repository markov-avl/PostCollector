from typing import final


@final
class TextUtility:

    @staticmethod
    def remove_indents(text: str) -> str:
        return "\n".join(s.strip() for s in text.strip().split("\n"))
