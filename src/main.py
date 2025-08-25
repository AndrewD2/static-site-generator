import shutil
import os

from extracttitle import extract_title
from markdowntohtml import markdown_to_html_node



def main():
    destination = "public"
    source = "static"
    from_path = "content/index.md"
    template_path = "template.html"
    dest_path = "public/index.html"

    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    source_to_destination(source, destination)
    generate_pages_recursive("content", template_path, "public")

def source_to_destination(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    dir_list = os.listdir(source)
    for item in dir_list:
        full_path = os.path.join(source, item)
        if os.path.isfile(full_path):
            print(f"copying {full_path} to {destination}")
            shutil.copy(full_path, destination)
        else:
            dest_path = os.path.join(destination, item)
            source_to_destination(full_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown_contet = f.read()
    with open(template_path, 'r') as f:
        template_content = f.read()
    html = markdown_to_html_node(markdown_contet).to_html()
    title = extract_title(markdown_contet)
    title_template = template_content.replace("{{ Title }}", title)
    filled_template = title_template.replace("{{ Content }}", html)
    dest_dirs = os.path.dirname(dest_path)
    os.makedirs(dest_dirs, exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(filled_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    with open(template_path, 'r') as f:
        template_content = f.read()
    for entry in os.listdir(dir_path_content):
        
        full_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(full_path):
            if full_path.endswith(".md"):
                with open(full_path, 'r') as f:
                    markdown_content = f.read()
                relative_path = os.path.relpath(full_path, "content")
                dest_path = os.path.join("public", relative_path)
                dest_path = os.path.splitext(dest_path)[0] + ".html"
                html = markdown_to_html_node(markdown_content).to_html()
                title = extract_title(markdown_content)
                title_template = template_content.replace("{{ Title }}", title)
                filled_template = title_template.replace("{{ Content }}", html)
                dest_dirs = os.path.dirname(dest_path)
                os.makedirs(dest_dirs, exist_ok=True)
                with open(dest_path, 'w') as f:
                    f.write(filled_template)            
        elif os.path.isdir(full_path):
            sub_dest_dir = os.path.join("public", os.path.relpath(full_path, "content"))
            generate_pages_recursive(full_path, template_path, sub_dest_dir)

main()
