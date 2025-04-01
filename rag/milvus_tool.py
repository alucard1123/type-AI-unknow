from flask import current_app
from docx import Document
from sentence_transformers import SentenceTransformer

collection_name = "rag_collection"
transformer_model_path = 'C:/Users/yulong/Desktop/bert/bert-master/project/type_AI_unknow/lib/all-MiniLM-L6-v2'


def save_data_to_milvus(raw_data:list):
    # 获取 Milvus 客户端
    client = current_app.config['MILVUS_CLIENT']

    if not client.has_collection(collection_name):
        client.create_collection(
            collection_name=collection_name,
            dimension=384,  # 使用 Sentence Transformer 的维度
            auto_id = True

        )

    # 加载 Sentence Transformer 模型
    model = SentenceTransformer(transformer_model_path)
    # 对文档进行编码
    vectors = model.encode(raw_data)

    # 构造数据 如果主键id自增，则不需要手动添加id
    # last_id = search_last_id()
    data = [
        {"id": i, "vector": vector.tolist(), "text": raw_data[i], "subject": "history"}
        # {"vector": vector.tolist(), "text": docs[i], "subject": "history"}
        for i, vector in enumerate(vectors)
    ]

    # 插入数据到 Milvus
    client.insert(
        collection_name=collection_name,
        data=data
    )
    print(f"Inserted {len(data)} documents into Milvus.")


# def search_last_id():
#     last_id = 0
#     # 初始化 Milvus 客户端
#     client = current_app.config['MILVUS_CLIENT']
#     # 确保集合存在
#     if client.has_collection(collection_name):
#         # 查询最新一条数据的 id
#         res = client.query(
#             collection_name=collection_name,
#             filter="",
#             output_fields=["id"],  # 仅返回主键 id 字段
#             limit=1,  # 限制返回 1 条数据
#             order_by="id DESC"  # 按照 id 降序排序
#         )
#
#         if res:
#             last_id = res[0]["id"]  # 获取最新记录的 id
#     return last_id


def serch_data_from_milvus(query_data, filter='', output_fields=None, limit=3):
    print(query_data)
    if output_fields is None:
        output_fields = ["text", "subject"]

    client = current_app.config['MILVUS_CLIENT']
    if not client.has_collection(collection_name):
        client.create_collection(
            collection_name=collection_name,
            dimension=384,  # 使用 Sentence Transformer 的维度
        )

    # 加载 Sentence Transformer 模型
    model = SentenceTransformer(transformer_model_path)

    query_vector = model.encode([query_data])

    # 在 Milvus 中搜索相似文档
    res = client.search(
        collection_name=collection_name,
        data=query_vector.tolist(),
        filter=filter,
        limit=limit,
        output_fields=output_fields,
    )
    return res

#################插入docx数据经数据库#########################
def save_docx_to_milvus(docx_path):
    # 从 DOCX 文件中读取文本内容
    raw_data = read_docx(docx_path)
    print("读取的文档内容：", raw_data)
    save_data_to_milvus(raw_data)


def read_docx(file_path):
    document = Document(file_path)
    full_text = []
    for para in document.paragraphs:
        if para.text.strip():  # 只添加非空段落
            full_text.append(para.text)
    return full_text
