import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is also a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_different_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


# test text_node_to_html_node
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

# stolen tests
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


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

if __name__ == "__main__":
    unittest.main()
