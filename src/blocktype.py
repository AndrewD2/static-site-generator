from enum import Enum

class BlockType(Enum):
    PARAGRAPH      = "paragraph"
    HEADING        = "heading"
    CODE           = "code"
    QUOTE          = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST   = "ordered_list"


def block_to_block_type(block):
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return BlockType.HEADING
    split_block = block.split("\n")
    is_ordered_list = True
    for i, line in enumerate(split_block):
        dot_index = line.find(".")
        if dot_index == -1:
            is_ordered_list = False
            break
        try:
            parsed_number = int(line[:dot_index])
            if dot_index > 0 and parsed_number == i + 1 and line[dot_index] == "." and len(line) > dot_index + 1 and line[dot_index+1] == " ":
                continue
            else:
                is_ordered_list = False
                break
        except ValueError:
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    is_unordred_list = True
    for line in split_block:
        try:
            if len(line) < 2:
                is_unordred_list = False
                break
            char = line[0]
            space = line[1]
            if char == "-" and space == " ":
                continue
            else:
              is_unordred_list = False
              break
        except:
            is_unordred_list = False
            break
    if is_unordred_list:
        return BlockType.UNORDERED_LIST
    is_quote = True
    for line in split_block:
        try:
            char = line[0]
            if char == ">":
                continue
            else:
              is_quote = False
              break
        except:
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    return BlockType.PARAGRAPH