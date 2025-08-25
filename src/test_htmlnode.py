import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(tag="a", value="link", props={"href": "http://www.boot.dev", "target":"_blank"})
        self.assertEqual(node.props_to_html(), ' href="http://www.boot.dev" target="_blank"')
    

if __name__ == "__main__":
    unittest.main()