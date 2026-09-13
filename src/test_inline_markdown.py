import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
# test split_nodes_delimiter
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_split2(self):
        node = TextNode("This is text doesn't contain the delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [TextNode("This is text doesn't contain the delimiter", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_result)

    def test_split3(self):
        node = TextNode("This is +text+ contains the delimiter", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "+", TextType.BOLD)
        expected_result = [TextNode("This is +text+ contains the delimiter", TextType.ITALIC)]
        self.assertEqual(new_nodes, expected_result)

    def test_split_multiple(self):
        nodes = [
            TextNode("This is **text** contains the delimiter", TextType.BOLD),
            TextNode("This is **text** contains the delimiter", TextType.TEXT),
            TextNode("This is text doesn't contain the delimiter", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.ITALIC)
        expected_result = [
            TextNode("This is **text** contains the delimiter", TextType.BOLD),
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.ITALIC),
            TextNode(" contains the delimiter", TextType.TEXT),
            TextNode("This is text doesn't contain the delimiter", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_raises_unmatched(self):
        node = TextNode("This is **text** contains unmatched ** of the delimiter", TextType.TEXT)
        self.assertRaises(ValueError, lambda: split_nodes_delimiter([node], "**", TextType.CODE))

    def test_no_prefix(self):
        node = TextNode("'This text contains' no prefix", TextType.TEXT)
        expected = [
            TextNode("This text contains", TextType.CODE),
            TextNode(" no prefix", TextType.TEXT)
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "'", TextType.CODE),
            expected
        )

    def test_no_suffix(self):
        node = TextNode("This text contains' no suffix'", TextType.TEXT)
        expected = [
            TextNode("This text contains", TextType.TEXT),
            TextNode(" no suffix", TextType.CODE)
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "'", TextType.CODE),
            expected
        )

    def test_no_content(self):
        node = TextNode("This code block '' is empty", TextType.TEXT)
        expected = [
            TextNode("This code block ", TextType.TEXT),
            TextNode(" is empty", TextType.TEXT)
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "'", TextType.CODE),
            expected
        )

    def test_only_code(self):
        node = TextNode("'only code'", TextType.TEXT)
        expected = [
            TextNode("only code", TextType.CODE)
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "'", TextType.CODE),
            expected
        )

    def test_text_block(self):
        node = TextNode("This is 'just' text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("just", TextType.TEXT),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "'", TextType.TEXT),
            expected
        )

    def test_multiple_blocks(self):
        node = TextNode("This 'contains' multiple' code blocks' in the text", TextType.TEXT)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("contains", TextType.CODE),
            TextNode(" multiple", TextType.TEXT),
            TextNode(" code blocks", TextType.CODE),
            TextNode(" in the text", TextType.TEXT)
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "'", TextType.CODE),
            expected
        )

# stolen tests
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


# test image, link extraction
    def test_link_does_not_match_image(self):
        matches = extract_markdown_links(
            "[link1](url1) then ![img1](url2) then [link2](url3)"
        )
        self.assertListEqual(
            [
                ("link1", "url1"),
                ("link2", "url3")
            ],
            matches
        )

    def test_image_does_not_match_link(self):
        matches = extract_markdown_images(
            "![img1](url1) then [link](url2) then ![img2](url3)"
        )
        self.assertListEqual(
            [
                ("img1", "url1"),
                ("img2", "url3")
            ],
            matches
        )

    def test_no_match_image(self):
        self.assertEqual(
            extract_markdown_images("No image"),
            []
        )

    def test_no_match_link(self):
        self.assertEqual(
            extract_markdown_links("No image"),
            []
        )

# stolen, can't be bothered to test regex
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://wikipedia.org"),
            ],
            matches,
        )


# test link, image splitting
    def test_split_no_image(self):
        self.assertEqual(
            split_nodes_image([TextNode("link", TextType.TEXT)]),
            [TextNode("link", TextType.TEXT)]
        )

    def test_split_no_link(self):
        self.assertEqual(
            split_nodes_image([TextNode("No link", TextType.TEXT)]),
            [TextNode("No link", TextType.TEXT)]
        )

    def test_link_does_not_split_image(self):
        matches = split_nodes_link(
            [
                TextNode(
                    "[link1](url1) then ![img1](url2) then [link2](url3)",
                    TextType.TEXT
                )
            ]
        )
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" then ![img1](url2) then ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url3")
            ],
            matches
        )

    def test_image_does_not_split_link(self):
        matches = split_nodes_image(
            [
                TextNode(
                    "![img1](url1) then [link](url2) then ![img2](url3)",
                    TextType.TEXT
                )
            ]
        )
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode(" then [link](url2) then ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "url3")
            ],
            matches
        )

    def test_text_does_not_change_link(self):
        matches = split_nodes_link(
            [
                TextNode("![img1](url1) then [link](url2) then ![img2](url3)", TextType.CODE),
                TextNode(
                    "[link1](url1) then ![img1](url2) then [link2](url3)",
                    TextType.TEXT
                ),
                TextNode("![img1](url1) then [link](url2) then ![img2](url3)", TextType.CODE)
            ]
        )
        self.assertListEqual(
            [
                TextNode("![img1](url1) then [link](url2) then ![img2](url3)", TextType.CODE),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" then ![img1](url2) then ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url3"),
                TextNode("![img1](url1) then [link](url2) then ![img2](url3)", TextType.CODE)
            ],
            matches
        )

    def test_text_does_not_change_image(self):
        matches = split_nodes_image(
            [
                TextNode("![img1](url1) then [link](url2) then ![img2](url3)", TextType.CODE),
                TextNode(
                    "![img1](url1) then [link](url2) then ![img2](url3)",
                    TextType.TEXT
                ),
                TextNode("![img1](url1) then [link](url2) then ![img2](url3)", TextType.CODE)
            ]
        )
        self.assertListEqual(
            [
                TextNode("![img1](url1) then [link](url2) then ![img2](url3)", TextType.CODE),
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode(" then [link](url2) then ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "url3"),
                TextNode("![img1](url1) then [link](url2) then ![img2](url3)", TextType.CODE)
            ],
            matches
        )

# stolen tests, fuck regex
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://wikipedia.org"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )


# text to textnodes
def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

def test_to_textnodes_without_space(self):
        nodes = text_to_textnodes(
            "**text**_italic_`code block`![image](https://i.imgur.com/zjjcJKZ.png)[link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("text", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code block", TextType.CODE),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()
