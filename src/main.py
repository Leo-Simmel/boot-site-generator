from textnode import TextNode, TextType


def main():
    example_node = TextNode("hello world", TextType.PLAIN_TEXT, "http://localhost:8888")
    print(example_node)

if __name__ == "__main__":
    main()
