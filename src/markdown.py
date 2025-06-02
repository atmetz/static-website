from textnode import TextNode, TextType

import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            new_node = old_node.text.split(delimiter)
            if len(new_node) != 3:
                raise Exception(f"No closing delimiter found: {delimiter}")
            new_node1 = [TextNode(f"{new_node[0]}", TextType.TEXT),
                         TextNode(f"{new_node[1]}", text_type),
                         TextNode(f"{new_node[2]}", TextType.TEXT)]
            new_nodes.extend(new_node1)


    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches