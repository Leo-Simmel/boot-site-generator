import re
from enum import Enum

from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    return [
        line.strip()
        for line in markdown.split("\n\n")
        if line != ""
    ]


HEADING_PATTERN = re.compile(r"^#{1,6} (.+)$")
HEADING_INDENT = re.compile(r"(#{1,6})")
CODE_PATTERN = re.compile(r"^`{3}\n(.*)`{3}$", re.DOTALL)
QUOTE_PATTERN = re.compile(r"^(?:>.*\n?)+$")
QUOTE_CONTENT = re.compile(r"^>(.*)", re.MULTILINE)
ULIST_PATTERN = re.compile(r"^(?:- .*\n?)+$")
ULIST_CONTENT = re.compile(r"^- (.*)", re.MULTILINE)
OLIST_PATTERN = re.compile(r"^(?:\d+\. .*\n?)+$")
OLIST_INDEX = re.compile(r"^(\d+)\. ", re.MULTILINE)
OLIST_CONTENT = re.compile(r"^\d+\. (.*)", re.MULTILINE)

def block_to_block_type(block: str) -> BlockType:
    if HEADING_PATTERN.search(block):
        return BlockType.HEADING
    if CODE_PATTERN.search(block):
        return BlockType.CODE
    if QUOTE_PATTERN.search(block):
        return BlockType.QUOTE
    if ULIST_PATTERN.search(block):
        return BlockType.ULIST
    # olist
    if OLIST_PATTERN.search(block):
        matches = OLIST_INDEX.findall(block)
        # ensure the list index iterates sequentially from one
        if all(str(num) == match for num, match in enumerate(matches, start=1)):
            return BlockType.OLIST

    return BlockType.PARAGRAPH

def block_to_block_type_with_content(block: str) -> tuple[BlockType, str | list[str]]:
    match = HEADING_PATTERN.search(block)
    if match is not None:
        return BlockType.HEADING, match.group(1)
    match = CODE_PATTERN.search(block)
    if match is not None:
        return BlockType.CODE, match.group(1)
    if QUOTE_PATTERN.search(block) is not None:
        return BlockType.QUOTE, " ".join(
            line.strip()
            for line in QUOTE_CONTENT.findall(block)
        )
    if ULIST_PATTERN.search(block):
        return BlockType.ULIST, ULIST_CONTENT.findall(block)
    # olist
    if OLIST_PATTERN.search(block):
        indeces = OLIST_INDEX.findall(block)
        # ensure the list index iterates sequentially from one
        if all(str(num) == match for num, match in enumerate(indeces, start=1)):
            return BlockType.OLIST, OLIST_CONTENT.findall(block)

    return BlockType.PARAGRAPH, " ".join(line.strip() for line in block.split())

def text_to_children(text: str) -> list[HTMLNode]:
    return [
        text_node_to_html_node(node)
        for node in text_to_textnodes(text)
    ]

def markdown_to_html_node(markdown) -> HTMLNode:
    main_children = []
    for block in markdown_to_blocks(markdown):
        type, content = block_to_block_type_with_content(block)
        match type:
            case BlockType.CODE:
                assert isinstance(content, str)
                code_node = LeafNode("code", content)
                preformatted = ParentNode("pre", [code_node])
                main_children.append(preformatted)
                # special case, don't process inline markdown
                continue
            case BlockType.PARAGRAPH:
                assert isinstance(content, str)
                children = text_to_children(content)
                main_children.append(
                    ParentNode("p", children)
                )
            case BlockType.HEADING:
                assert isinstance(content, str)
                children = text_to_children(content)
                # TODO: make heading be based on number of hash signs
                match = HEADING_INDENT.match(block)
                assert match is not None
                level = match.end(1) - match.start(1)
                main_children.append(
                    ParentNode(f"h{level}", children)
                )
            case BlockType.QUOTE:
                assert isinstance(content, str)
                children = text_to_children(content)
                main_children.append(
                    ParentNode("blockquote", children)
                )
            case BlockType.ULIST:
                assert isinstance(content, list)
                list_node = ParentNode("ul",
                    [
                        ParentNode("li",
                            text_to_children(line)
                        )
                        for line in content
                    ]
                )
                main_children.append(list_node)
            case BlockType.OLIST:
                assert isinstance(content, list)
                list_node = ParentNode("ol",
                    [
                        ParentNode("li",
                            text_to_children(line)
                        )
                        for line in content
                    ]
                )
                main_children.append(list_node)

    if len(main_children) == 0:
        return LeafNode(None, "")

    return ParentNode("div", main_children)
