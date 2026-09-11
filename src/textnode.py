from enum import Enum


class TextType(Enum):
    PLAIN_TEXT = "text"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINKS = "link"
    IMAGES = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
                    return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
