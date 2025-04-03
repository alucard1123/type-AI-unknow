# 这个工具是用来根据data文件夹中的文件插入到milvus数据库， 提供新的文件存储， 向量去重， 重建等数据的的存储功能。


"""存储新的data文件
input file: 文件名或者文件夹
"""
import os

from flask import current_app
from sentence_transformers import SentenceTransformer

import project.type_AI_unknow.util.file_util


def store_new(file):
    # 检查是否为文件夹
    if project.type_AI_unknow.util.file_util.is_folder(file):
        # 如果是文件夹，遍历文件夹中的所有文件
        for root, _, files in os.walk(file):
            for filename in files:
                # 筛选出 .docx 文件
                if filename.endswith(".docx"):
                    file_path = os.path.join(root, filename)
                    # 调用 _store_single_file 存储单个文件
                    _store_single_file(project.type_AI_unknow.util.file_util.read_word_text(file_path))
    else:
        # 如果是单个文件，直接读取内容并存储
        if file.endswith(".docx"):
            _store_single_file(project.type_AI_unknow.util.file_util.read_word_text(file))


def _store_single_file(rawdata:list):
    collection_name = current_app.config.get('COLLECTION_NAME')
    client = current_app.config['MILVUS_CLIENT']
    if not client.has_collection(collection_name):
        client.create_collection(
            collection_name=collection_name,
            dimension=384,  # 使用 Sentence Transformer 的维度
            auto_id=True

        )
    # 加载 Sentence Transformer 模型
    model = SentenceTransformer(transformer_model_path)
    # 对文档进行编码
    vectors = model.encode(rawdata)

    # 构造数据 如果主键id自增，则不需要手动添加id
    # last_id = search_last_id()
    data = [
        {"id": i, "vector": vector.tolist(), "text": rawdata[i], "subject": "history"}
        for i, vector in enumerate(vectors)
    ]

    # 插入数据到 Milvus
    client.insert(
        collection_name=collection_name,
        data=data
    )
    pass
