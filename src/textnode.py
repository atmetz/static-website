from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode

# Define text types
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

# Define text node class. 
# text -> text content of node
# text_type -> type of text the node contains
# url -> url of link or image. Default to None

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    # For Unit tests, returns True if equal
    def __eq__(self, other):
        return (self.text == other.text and self.text_type == other.text_type and self.url == other.url)

    # Returns string representation of TextNOde
    # TextNode(TEXT, TEXT_TYPE, URL)
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    


def text_node_to_html_node(text_node):
    # return LeafNode with no tag
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    # return LeafNode with b tag and text
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    # return LeafNode with i tag and text
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    # return LeafNode with code tag and text
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)    
    # return LeafNode with a tag, anchor text and href prop
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    # return LeafNode with img tag , empty string value, src and alt props
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    # if none of the above, ValueError
    raise ValueError(f"invalid text type: {text_node.text_type}")