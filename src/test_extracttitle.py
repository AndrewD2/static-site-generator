import unittest
from extracttitle import extract_title

class TestBlockType(unittest.TestCase):
    def test_title(self):
        block = "# TITLE "
        self.assertEqual(extract_title(block), "TITLE")

    def test_no_title(self):
        block = "## TITLE"
        with self.assertRaises(Exception):
            extract_title(block)