from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
            self,
            tag: str,
            children: list["HTMLNode"],
            props: dict[str, str] | None = None
            ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("invalid HTML: no tag")
        if not self.children or len(self.children) < 1:
            raise ValueError("invalid HTML: no children")
        children_string = "".join(child.to_html() for child in self.children)
        return f'<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>'

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
