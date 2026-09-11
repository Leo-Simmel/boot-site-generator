import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_default(self):
        node = HTMLNode()
        self.assertIs(node.tag, None)
        self.assertIs(node.value, None)
        self.assertIs(node.children, None)
        self.assertIs(node.props, None)

    def test_props_repr(self):
        attributes = {
            "href": "https://www.google.com",
            "target": "_blank"
        }
        node = HTMLNode(props=attributes)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_convert_empty_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_single_attribute_props(self):
        node = HTMLNode(props={"key": "value"})
        self.assertEqual(node.props_to_html(), ' key="value"')

    def test_no_implementation(self):
        self.assertRaises(NotImplementedError, HTMLNode().to_html)

# stolen from solution
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )


if __name__ == "__main__":
    unittest.main()
