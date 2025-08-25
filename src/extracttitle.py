

from helpers import markdown_to_blocks


def extract_title(markdown):
    title = ""
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            title = block[2:].strip()
            return title
        else:
            continue
    raise Exception("No title found")