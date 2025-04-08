import os

from docx import Document

def is_folder(path):
    return os.path.isdir(path)

def get_files(path):
    return os.listdir(path)

def read_word_text(file_path):
    document = Document(file_path)
    full_text = []
    for para in document.paragraphs:
        if para.text.strip():  # 只添加非空段落
            full_text.append(para.text)
    return full_text

def get_abs_path(path):
    return os.path.abspath(path)

def get_all_sub_path(path):
    subpaths = []
    for root, dirs, files in os.walk(path):
        # 获取所有文件路径
        file_paths = [os.path.join(root, file) for file in files]
        subpaths.extend(file_paths)
        # 获取所有目录路径
        dir_paths = [os.path.join(root, d) for d in dirs]
        subpaths.extend(dir_paths)
    return subpaths