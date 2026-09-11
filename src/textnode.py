from enum import Enum


class TextType(Enum):
    PLAIN_TEXT = 0
    BOLD_TEXT = 1
    ITALIC_TEXT = 2
    CODE_TEXT = 3
    LINKS = 4
    IMAGES = 5

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
