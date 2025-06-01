import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_url(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("i", "child2")
        child_node3 = LeafNode("b", "child3")
        child_node4 = LeafNode("p", "child4")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3, child_node4])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><i>child2</i><b>child3</b><p>child4</p></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_url(self):
        child_node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        child_node2 = LeafNode("i", "child2")
        child_node3 = LeafNode("b", "child3")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), '<div><a href="https://www.google.com">Click me!</a><i>child2</i><b>child3</b></div>')

    def test_to_html_with_grandchildren(self):
        grandchild_node1 = LeafNode("a", "grandchild1", {"href": "https://www.google.com"})
        grandchild_node2 = LeafNode("i", "grandchild2")
        grandchild_node3 = LeafNode("b", "grandchild3")
        child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2, grandchild_node3])

        grandchild_node4 = LeafNode("d", "grandchild4")
        grandchild_node5 = LeafNode("a", "grandchild5", {"href": "https://www.google.com"})
        grandchild_node6 = LeafNode("p", "grandchild6")
        child_node2 = ParentNode("span", [grandchild_node4, grandchild_node5, grandchild_node6])

        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><a href="https://www.google.com">grandchild1</a><i>grandchild2</i><b>grandchild3</b></span>' \
            '<span><d>grandchild4</d><a href="https://www.google.com">grandchild5</a><p>grandchild6</p></span></div>'
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()