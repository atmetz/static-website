from textnode import TextNode, TextType

from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    temp = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(temp.__repr__())

main()
