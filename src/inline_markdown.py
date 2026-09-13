import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        # split node
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        new_nodes.extend(
            TextNode(section, TextType.TEXT if i % 2 == 0 else text_type)
            for i, section in enumerate(sections)
            if section != ""
        )

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    pattern = re.compile(r"!\[([^\]]*)\]\(([^)]*)\)")
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # split_oldnode
        node_text = old_node.text
        pos = 0
        for match in pattern.finditer(node_text):
            if match.start() > pos:
                new_nodes.append(TextNode(node_text[pos:match.start()], TextType.TEXT))

            new_nodes.append(
                TextNode(
                    match.group(1),
                    TextType.IMAGE,
                    match.group(2)
                )
            )

            pos = match.end()

        if pos < len(node_text):
            new_nodes.append(TextNode(node_text[pos:], TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    pattern = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # split_oldnode
        node_text = old_node.text
        pos = 0
        for match in pattern.finditer(node_text):
            if match.start() > pos:
                new_nodes.append(TextNode(node_text[pos:match.start()], TextType.TEXT))

            new_nodes.append(
                TextNode(
                    match.group(1),
                    TextType.LINK,
                    match.group(2)
                )
            )

            pos = match.end()

        if pos < len(node_text):
            new_nodes.append(TextNode(node_text[pos:], TextType.TEXT))

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
