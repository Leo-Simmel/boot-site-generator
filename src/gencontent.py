import os

from block_markdown import extract_title, markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as from_file:
        markdown_content = from_file.read()
    with open(template_path, 'r') as template_file:
        template = template_file.read()

    html = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    processed = (
        template
        .replace("{{ Title }}", title, 1)
        .replace("{{ Content }}", html, 1)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, 'w') as to_file:
        to_file.write(processed)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(file_path):
            if not filename.endswith(".md"):
                raise ValueError(f"expected only markdown files in directory {dir_path_content}")
            dest_name = filename[:-3] + ".html"
            dest_path = os.path.join(dest_dir_path, dest_name)
            generate_page(file_path, template_path, dest_path, basepath)
            continue
        dir_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        generate_pages_recursive(dir_path, template_path, dest_path, basepath)
