import os
import shutil


def copy_files_recursive(source_dir_path: str, dest_dir_path: str) -> None:
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        src_path = os.path.join(source_dir_path, filename)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_dir_path)
            continue
        dest_path = os.path.join(dest_dir_path, filename)
        copy_files_recursive(src_path, dest_path)
