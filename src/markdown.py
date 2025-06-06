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
        if old_node.text == "":
            pass
        else:
            matches = extract_markdown_images(old_node.text)
            if len(matches) == 0:
                new_node.append(old_node)
            else:                
                split_node = []
                original_text = old_node.text
                for match in matches:
                    image_alt = match[0]
                    image_link = match[1]
                    sections = original_text.split(f"![{image_alt}]({image_link})", 1)
                    split_node.append(TextNode(f'{sections[0]}', TextType.TEXT))
                    split_node.append(TextNode(f'{image_alt}', TextType.IMAGE, f'{image_link}'))
                    original_text = sections[1]
                new_node.extend(split_node)

    return new_node

def split_nodes_link(old_nodes):
    new_node = []
    for old_node in old_nodes:
        if old_node.text == "":
            pass
        else:
            matches = extract_markdown_links(old_node.text)
            if len(matches) == 0:
                new_node.append(old_node)
            else:                
                split_node = []
                original_text = old_node.text
                for match in matches:
                    link_alt = match[0]
                    link = match[1]
                    sections = original_text.split(f"[{link_alt}]({link})", 1)
                    split_node.append(TextNode(f'{sections[0]}', TextType.TEXT))
                    split_node.append(TextNode(f'{link_alt}', TextType.LINK, f'{link}'))
                    original_text = sections[1]
                new_node.extend(split_node)

    return new_node

