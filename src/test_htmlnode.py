import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_empty_node(self):
      node = HTMLNode()
      self.assertIsNone(node.tag)
      self.assertIsNone(node.value)
      self.assertIsNone(node.children)
      self.assertIsNone(node.props)

    def test_node_representation(self):
      node = HTMLNode(tag="p", value="Hello, World!", children=[TextNode("Hello, World!", TextType.PLAIN)], props={"class": "greeting"})
      expected_repr = "HTMLNode(tag=p, value=Hello, World!, children=[TextNode(Hello, World!, TextType.PLAIN, None)], props={'class': 'greeting'})"
      self.assertEqual(repr(node), expected_repr)

    def test_props_to_html_no_props(self):
      node = HTMLNode(tag="div")
      self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_with_props(self):
      props = {
        "class": "container",
        "id": "main"
      }
      node = HTMLNode(tag="div", props=props)
      self.assertEqual(node.props_to_html(), ' class="container" id="main"')


class TestLeafNode(unittest.TestCase):
  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

  def test_leaf_to_html_div_with_props(self):
    props = {
      "class": "container",
      "id": "main"
    }
    node = LeafNode("div", "Content here", props=props)
    self.assertEqual(node.to_html(), '<div class="container" id="main">Content here</div>')

  def test_leaf_to_html_a_with_props(self):
    props = {
      "href": "https://www.example.com",
      "target": "_blank"
    }
    node = LeafNode("a", "Click here", props=props)
    self.assertEqual(node.to_html(), '<a href="https://www.example.com" target="_blank">Click here</a>')


class TestParentNode(unittest.TestCase):
  def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

  def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

  def test_to_html_with_multiple_children(self):
    child_node1 = LeafNode("p", "child1")
    child_node2 = LeafNode("p", "child2")
    parent_node = ParentNode("div", [child_node1, child_node2])
    self.assertEqual(
        parent_node.to_html(),
        "<div><p>child1</p><p>child2</p></div>",
    )

  def test_to_html_without_children(self):
    parent_node = ParentNode("div", [])
    with self.assertRaises(ValueError):
      parent_node.to_html()


if __name__ == "__main__":
    unittest.main()
