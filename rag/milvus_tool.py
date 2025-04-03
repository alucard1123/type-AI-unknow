from flask import current_app
from docx import Document
from sentence_transformers import SentenceTransformer

collection_name = "rag_collection"
transformer_model_path = 'C:/Users/yulong/Desktop/bert/bert-master/project/type_AI_unknow/lib/all-MiniLM-L6-v2'

#######################向量数据库操作###########################################
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
        for i, vector in enumerate(vectors)
    ]

    # 插入数据到 Milvus
    client.insert(
        collection_name=collection_name,
        data=data
    )


def serch_data_from_milvus(query_data, filter='', output_fields=None, limit=3):
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
    # 向量编码
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

#####################辅助方法################################
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
