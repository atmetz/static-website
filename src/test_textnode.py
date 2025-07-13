import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from markdown import (
    BlockType,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_links,
    extract_markdown_images,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

class TestSplitDelimiter(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        nodes = [node]
        text_type = TextType.BOLD

        new_nodes = split_nodes_delimiter(nodes, "**", text_type)
        ex_nodes = [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" word", TextType.TEXT),
                ]
        self.assertEqual(new_nodes, ex_nodes)

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        nodes = [node]
        text_type = TextType.CODE

        new_nodes = split_nodes_delimiter(nodes, "`", text_type)
        ex_nodes = [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.TEXT),
                ]
        self.assertEqual(new_nodes, ex_nodes)

    def test_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        nodes = [node]
        text_type = TextType.ITALIC

        new_nodes = split_nodes_delimiter(nodes, "_", text_type)
        ex_nodes = [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word", TextType.TEXT),
                ]
        self.assertEqual(new_nodes, ex_nodes)

class TestMarkdownRegx(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_images_mulitple(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links_mulitple(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_images_mulitple_combo(self):
        matches = extract_markdown_images(
            "This is text with a link ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif")], matches)

    def test_extract_markdown_links_mulitple_combo(self):
        matches = extract_markdown_links(
            "This is text with a link ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

class TestSplitDelimiter(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode(
            "This is text without an image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text without an image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_no_link(self):
        node = TextNode(
            "This is text without a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text without a link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )    

    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        #text_to_textnodes(text)
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        ) 

    def test_text_to_textnode2(self):
        text = "This is **text** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        ) 

    def test_text_to_textnode3(self):
        text = "This is _italic_ with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a **text** word and a [link](https://boot.dev) and a `code block`"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" with an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        md = """
This is **bolded** paragraph



    This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line    


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_unordered(self):
        md = "- This is a list\n- with items"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.UNORDERED_LIST
        )

    def test_block_to_block_type_ordered(self):
        md = "1. This is a list\n2. with items"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.ORDERED_LIST
        )

    def test_block_to_block_type_quote(self):
        md = ">This is a quote\n>mulitple"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.QUOTE
        )

    def test_block_to_block_type_code(self):
        md = "```This is a code\nblock with multiple lines```"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.CODE
        )
    def test_block_to_block_type_code_one_line(self):
        md = "```This is a code block with one line```"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.CODE
        )

    def test_block_to_block_type_heading_one(self):
        md = "#This is a heading block with one line"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.HEADING
        )

    def test_block_to_block_type_heading_two(self):
        md = "##This is a heading block with one line"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.HEADING
        )

    def test_block_to_block_type_heading_three(self):
        md = "###This is a heading block with one line"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.HEADING
        )

    def test_block_to_block_type_heading_four(self):
        md = "####This is a heading block with one line"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.HEADING
        )

    def test_block_to_block_type_heading_five(self):
        md = "#####This is a heading block with one line"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.HEADING
        )

    def test_block_to_block_type_heading_six(self):
        md = "######This is a heading block with one line"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.HEADING
        )

    def test_block_to_block_type_heading_six_extra(self):
        md = "#####This is a head#ing block with one line"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.HEADING
        )


if __name__ == "__main__":
    unittest.main()
