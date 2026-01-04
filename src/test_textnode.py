import unittest

from textnode import TextNode, TextType
import utils


class TestTextNode(unittest.TestCase):
    def test_eq(self):
      node = TextNode("This is a text node", TextType.BOLD)
      node2 = TextNode("This is a text node", TextType.BOLD)
      self.assertEqual(node, node2)
    
    def test_neq_diff_text(self):
      node1 = TextNode("This is a text node", TextType.BOLD)
      node2 = TextNode("This is a different text node", TextType.BOLD)
      self.assertNotEqual(node1, node2)

    def test_neq_diff_type(self):
      node1 = TextNode("This is a text node", TextType.BOLD)
      node2 = TextNode("This is a text node", TextType.ITALIC)
      self.assertNotEqual(node1, node2)

    def test_neq_diff_url(self):
      node1 = TextNode("This is a link", TextType.LINK, "https://example.com")
      node2 = TextNode("This is a link", TextType.LINK, "https://different.com")
      self.assertNotEqual(node1, node2)

    def test_neq_missing_url(self):
      node1 = TextNode("This is a link", TextType.LINK, "https://example.com")
      node2 = TextNode("This is a link", TextType.LINK)
      self.assertNotEqual(node1, node2)

    def test_text_to_html_plain(self):
      node = TextNode("This is a text node", TextType.PLAIN)
      html_node = TextNode.text_node_to_html_node(node)
      self.assertEqual(html_node.tag, None)
      self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html_bold(self):
      node = TextNode("Bold text", TextType.BOLD)
      html_node = TextNode.text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "b")
      self.assertEqual(html_node.value, "Bold text")

    def test_text_to_html_italic(self):
      node = TextNode("Italic text", TextType.ITALIC)
      html_node = TextNode.text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "i")
      self.assertEqual(html_node.value, "Italic text")

    def test_text_to_html_code(self):
      node = TextNode("print('hello')", TextType.CODE)
      html_node = TextNode.text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "code")
      self.assertEqual(html_node.value, "print('hello')")

    def test_text_to_html_link(self):
      node = TextNode("Click me", TextType.LINK, "https://example.com")
      html_node = TextNode.text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "a")
      self.assertEqual(html_node.value, "Click me")
      self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_to_html_image(self):
      node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
      html_node = TextNode.text_node_to_html_node(node)
      self.assertEqual(html_node.tag, "img")
      self.assertEqual(html_node.value, "")
      self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Alt text"})

    def test_split_nodes_single_instance(self):
      old_nodes = [TextNode("This is **bold** text", TextType.PLAIN)]
      delimiter = "**"
      text_type = TextType.BOLD
      split_nodes = utils.split_nodes_delimiter(old_nodes, delimiter, text_type)
      expected_nodes = [
        TextNode("This is ", TextType.PLAIN),
        TextNode("bold", TextType.BOLD),
        TextNode(" text", TextType.PLAIN)
      ]
      self.assertEqual(split_nodes, expected_nodes)

    def test_split_nodes_multiple_instances(self):
      old_nodes = [TextNode("This is **bold** text with more **bold** text", TextType.PLAIN)]
      delimiter = "**"
      text_type = TextType.BOLD
      split_nodes = utils.split_nodes_delimiter(old_nodes, delimiter, text_type)
      expected_nodes = [
        TextNode("This is ", TextType.PLAIN),
        TextNode("bold", TextType.BOLD),
        TextNode(" text with more ", TextType.PLAIN),
        TextNode("bold", TextType.BOLD),
        TextNode(" text", TextType.PLAIN)
      ]
      self.assertEqual(split_nodes, expected_nodes)

    def test_split_nodes_no_instances(self):
      old_nodes = [TextNode("This is plain text", TextType.PLAIN)]
      delimiter = "**"
      text_type = TextType.BOLD
      split_nodes = utils.split_nodes_delimiter(old_nodes, delimiter, text_type)
      expected_nodes = [TextNode("This is plain text", TextType.PLAIN)]
      self.assertEqual(split_nodes, expected_nodes)

    def test_split_nodes_multiple_nodes_same_type(self):
      old_nodes = [
        TextNode("This is **bold** text", TextType.PLAIN),
        TextNode("Another **bold** word here", TextType.PLAIN)
      ]
      delimiter = "**"
      text_type = TextType.BOLD
      split_nodes = utils.split_nodes_delimiter(old_nodes, delimiter, text_type)
      expected_nodes = [
        TextNode("This is ", TextType.PLAIN),
        TextNode("bold", TextType.BOLD),
        TextNode(" text", TextType.PLAIN),
        TextNode("Another ", TextType.PLAIN),
        TextNode("bold", TextType.BOLD),
        TextNode(" word here", TextType.PLAIN)
      ]
      self.assertEqual(split_nodes, expected_nodes)

    def test_split_nodes_multiple_delimiters(self):
      old_nodes = [TextNode("This is **bold** and *italic* text", TextType.PLAIN)]
      # First pass: split on bold
      nodes_after_bold = utils.split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
      # Second pass: split on italic
      split_nodes = utils.split_nodes_delimiter(nodes_after_bold, "*", TextType.ITALIC)
      expected_nodes = [
        TextNode("This is ", TextType.PLAIN),
        TextNode("bold", TextType.BOLD),
        TextNode(" and ", TextType.PLAIN),
        TextNode("italic", TextType.ITALIC),
        TextNode(" text", TextType.PLAIN)
      ]
      self.assertEqual(split_nodes, expected_nodes)

if __name__ == "__main__":
    unittest.main()
