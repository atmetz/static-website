from textnode import TextNode, TextType
from enum import Enum

import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
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

def markdown_to_html_node(markdown):

    markdown_blocks = markdown_to_blocks(markdown)

    for markdown_block in markdown_blocks:
        block_type = block_to_block_type(markdown_block)