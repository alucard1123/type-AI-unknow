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