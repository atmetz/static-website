from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from enum import Enum

import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

# define aplit_nodes_delimiter function
# Takes a list of old ondes, delimiter, and text type.
# Returns a new list of nodes, split by text type nodes into multiple nodes based on syntax.
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        # add to new_nodes if the text type is not TEXT
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        # SPlit old_node into sections by delimiter
        sections = old_node.text.split(delimiter)
        # Raise ValueError if closing delimiter is not found
        if len(sections) % 2 == 0:
            raise ValueError(f"No closing delimiter found: {delimiter}")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_node = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_node.append(old_node)
            continue
        original_text = old_node.text
        matches = extract_markdown_images(old_node.text)
        if len(matches) == 0:
            new_node.append(old_node)
            continue            
        for match in matches:
            sections = original_text.split(f"![{match[0]}]({match[1]})", 1)
            if sections[0] != "":
                new_node.append(TextNode(sections[0], TextType.TEXT))
            new_node.append(TextNode(match[0], TextType.IMAGE, match[1]))
            original_text = sections[1]
        if original_text != "":
            new_node.append(TextNode(original_text, TextType.TEXT))

    return new_node

def split_nodes_link(old_nodes):
    new_node = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_node.append(old_node)
            continue
        original_text = old_node.text
        matches = extract_markdown_links(old_node.text)
        if len(matches) == 0:
            new_node.append(old_node)
            continue
        for match in matches:
            sections = original_text.split(f"[{match[0]}]({match[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_node.append(TextNode(sections[0], TextType.TEXT))
            new_node.append(TextNode(match[0], TextType.LINK, match[1]))
            original_text = sections[1]
        if original_text != "":
            new_node.append(TextNode(original_text, TextType.TEXT))

    return new_node

def text_to_textnodes(text):
    original_text = [TextNode(text, TextType.TEXT)]
    original_text = (split_nodes_delimiter(original_text, "**", TextType.BOLD))
    original_text = (split_nodes_delimiter(original_text, "_", TextType.ITALIC))
    original_text = (split_nodes_delimiter(original_text, "`", TextType.CODE))
    original_text = (split_nodes_image(original_text))
    original_text = (split_nodes_link(original_text))

    return original_text

def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    new_markdown = []
    for line in lines:
        if line == "":
            continue
        new_markdown.append(line.strip())

    return new_markdown

def block_to_block_type(markdown):
    quote = True
    unordered = True
    ordered = True
    sections = markdown.split("\n")
    count = 0
    for section in sections:
        for letter in section:
            if letter == '#':
                count += 1
            if letter != '#':
                break
    if count > 0 and count <= 6:
        return BlockType.HEADING

    if sections[0][0:3] == "```" and sections[-1][-3:] == "```":
        return BlockType.CODE
    
    for line in sections:
        if line[0] != '>':
            quote = False
        if line[0] != '-':
            unordered = False
        if not re.findall(r"\d\.", line):
            ordered = False

    if quote:
        return BlockType.QUOTE
    if unordered:
        return BlockType.UNORDERED_LIST
    if ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

# Convert markdown text to html node
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)