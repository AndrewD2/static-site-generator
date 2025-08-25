import unittest
from blocktype import *

class TestBlockType(unittest.TestCase):

    def test_code_block(self):
        block = "```CODE BLOCK```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_ordered_list_block(self):
        block = "1. monkey\n2. star\n3. taco"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)