import os

from block_markdown import extract_title, markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as from_file:
        markdown_content = from_file.read()
    with open(template_path) as template_file:
        template = template_file.read()

    html = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    processed = template.replace("{{ Title }}", title, 1).replace("{{ Content }}", html, 1)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, 'w') as to_file:
        to_file.write(processed)
