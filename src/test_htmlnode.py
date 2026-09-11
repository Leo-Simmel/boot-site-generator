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

if __name__ == "__main__":
    unittest.main()
