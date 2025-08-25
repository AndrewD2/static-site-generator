from blocktype import BlockType, block_to_block_type
from helpers import *
from htmlnode import HTMLNode
import re
import textwrap

def markdown_to_html_node(markdown):
    block_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        if type == BlockType.CODE:
            lines = block.splitlines()
            code_content = "\n".join(lines[1:-1]) + "\n"
            code_content = textwrap.dedent(code_content)
            code = TextNode(code_content, TextType.CODE)
            html = text_node_to_html_node(code)
            pre = HTMLNode("pre", children=[html])
            block_nodes.append(pre)
        elif type == BlockType.UNORDERED_LIST or type == BlockType.ORDERED_LIST:
            lines = block.splitlines()
            li_nodes = []
            for line in lines:
                if not line.strip():
                    continue
                text = ""
                if type == BlockType.UNORDERED_LIST:
                    if line.startswith("- "):
                        text = line[2:]
                    elif line.startswith("* "):
                        text = line[2:]
                    elif line.startswith("+ "):
                        text = line[2:]
                elif type == BlockType.ORDERED_LIST:
                    text = re.sub(r"^\d+\.\s+", "", line)
                
                children = text_to_children(text)
                li_node = HTMLNode("li", children=children)
                li_nodes.append(li_node)
            correct_tag = block_type_to_tag(block, type)
            ul_or_ol = HTMLNode(correct_tag, children=li_nodes)
            block_nodes.append(ul_or_ol)
        else:
            if type == BlockType.PARAGRAPH:
                cleaned_text = " ".join(block.split())
                children = text_to_children(cleaned_text)
            elif type == BlockType.HEADING:
                first_word = block.split(" ")[0]
                heading_level = len(first_word)
                cleaned_text = block[heading_level:].strip()
                children = text_to_children(cleaned_text)
            elif type == BlockType.QUOTE:
                lines = block.splitlines()
                collected = []
                for line in lines:
                    if not line.strip():
                        continue
                    if line.startswith("> "):
                        text = line[2:].strip()
                    elif line.startswith(">"):
                        text = line[1:].strip()
                    collected.append(text)
                cleaned_text = "\n".join(collected) + "\n"
                children = text_to_children(cleaned_text)
            else:
                children = text_to_children(block)
            correct_tag = block_type_to_tag(block, type)
            html_node = HTMLNode(correct_tag, children=children)
            block_nodes.append(html_node)

    return HTMLNode("div", children=block_nodes)