from textnode import TextNode, TextType

import re

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

