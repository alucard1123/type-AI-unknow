from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer
import numpy as np
from docx import Document

# 读取 .docx 文件并提取所有段落的文本
def read_docx(file_path):
    document = Document(file_path)
    full_text = []
    for para in document.paragraphs:
        if para.text.strip():  # 只添加非空段落
            full_text.append(para.text)
    return full_text

# 读取 .docx 文件的数据
doc_file_path = '../data/如何写prd.docx'  # 替换为你的 .docx 文件路径
docs = read_docx(doc_file_path)
print(f"Loaded {len(docs)} paragraphs from the document.")
print()
for i in docs:
    print(i)
    print('////////////////////////')


#### 插入数据到数据库

token = '51094bff1288f58024b91453974a7f0352b7964d796bbe862e108a78438d2cc4172065ebae780cf8f704b47aa9c1e820c6fe20d2'
uri = 'https://in03-e7cec74bc4496b3.serverless.gcp-us-west1.cloud.zilliz.com'
client = MilvusClient(uri=uri,token=token)

# 创建集合
collection_name = "rag_collection"
if not client.has_collection(collection_name):
    client.create_collection(
        collection_name=collection_name,
        dimension=384,  # 使用 Sentence Transformer 的维度
    )
    print(f"Collection '{collection_name}' created.")
else:
    print(f"Collection '{collection_name}' already exists.")

# 加载 Sentence Transformer 模型
model = SentenceTransformer('../../all-MiniLM-L6-v2')
# 对文档进行编码
vectors = model.encode(docs)

# 构造数据 如果主键id自增，则不需要手动添加id
data = [
    {"id": i, "vector": vector.tolist(), "text": docs[i], "subject": "history"}
    # {"vector": vector.tolist(), "text": docs[i], "subject": "history"}
    for i, vector in enumerate(vectors)
]

# 插入数据到 Milvus
client.insert(
    collection_name=collection_name,
    data=data
)
print(f"Inserted {len(data)} documents into Milvus.")
