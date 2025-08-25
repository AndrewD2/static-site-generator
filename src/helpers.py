


from blocktype import BlockType
from extractmarkdown import extract_markdown_images, extract_markdown_links
from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, props={"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
    elif text_node.text_type == TextType.LINE_BREAK:
        return LeafNode("br", "")
    else:
        raise Exception("invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes=[]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            n = node.text.split(delimiter)
            if len(n) % 2 == 0:
                raise Exception("Invalid Markdown Detected")
            for i in range(0,len(n)):
                if n[i] == "":
                    continue
                if i % 2 == 1:
                    x = TextNode(n[i], text_type)
                else:
                    x = TextNode(n[i], TextType.TEXT)
                new_nodes.append(x)
        
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            current_text = node.text
            images = extract_markdown_images(node.text)
            for alt, url in images:
                before, after = current_text.split(f"![{alt}]({url})", 1)
                if before != "":
                    new_nodes.append(TextNode(before, node.text_type))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                current_text = after
            if current_text != "":
                new_nodes.append(TextNode(current_text, node.text_type))
    return new_nodes
            
def split_nodes_link(old_nodes):
    new_nodes = []
    current_text = ""
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            current_text = node.text
            links = extract_markdown_links(node.text)
            for alt, url in links:
                before, after = current_text.split(f"[{alt}]({url})", 1)
                if before != "":
                    new_nodes.append(TextNode(before, node.text_type))
                new_nodes.append(TextNode(alt, TextType.LINK, url=url))
                current_text = after
            if current_text != "":
                new_nodes.append(TextNode(current_text, node.text_type))
    return new_nodes

def text_to_textnodes(text):
    current_nodes = [TextNode(text, TextType.TEXT)]
    
    newly_processed_nodes = []
    for node in current_nodes:
        if node.text_type != TextType.TEXT:
            newly_processed_nodes.append(node)
            continue

        parts = node.text.split("\n")
        for i, part in enumerate(parts):
            if part:
                newly_processed_nodes.append(TextNode(part, TextType.TEXT))
            if i < len(parts) - 1:
                newly_processed_nodes.append(TextNode("", TextType.LINE_BREAK))

    nodes = newly_processed_nodes
    
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes

def markdown_to_blocks(markdown):
    lines = markdown.splitlines()
    blocks = []
    current_block = []
    for line in lines:
        if line.strip() == "":
            if current_block:
                blocks.append("\n".join(current_block).strip())
                current_block = []
        else:
            current_block.append(line)
    if current_block:
        blocks.append("\n".join(current_block).strip())
    return blocks

def text_to_children(block):
    text_nodes = text_to_textnodes(block)
    html_children = [text_node_to_html_node(node) for node in text_nodes]
    return html_children

def block_type_to_tag(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        return "p"
    elif block_type == BlockType.QUOTE:
        return "blockquote"
    elif block_type == BlockType.ORDERED_LIST:
        return "ol"
    elif block_type == BlockType.UNORDERED_LIST:
       
        return "ul"
    elif block_type == BlockType.HEADING:
        first_word = block.split(" ")[0]
        heading_level = len(first_word)
        return f"h{heading_level}"
    