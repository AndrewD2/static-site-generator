import unittest

from leafnode import *


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    # def test_props(self):
    #     node = LeafNode(tag="a", value="link", props={"href": "http://www.boot.dev", "target":"_blank"})
    #     self.assertEqual(node.to_html(), '<a href="http://www.boot.dev" target="_blank">links</a>')
    
if __name__ == "__main__":
    unittest.main()