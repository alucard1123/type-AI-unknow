from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer
import numpy as np

# 初始化 Milvus Lite
# client = MilvusClient("./milvus_demo.db")
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


print("Sentence Transformer model loaded.")
#
# 示例查询
# query = "Who conducted substantial research in AI?"
query = "国内生产总值和生鲜的关系"

# 对查询进行编码
query_vector = model.encode([query])

# 在 Milvus 中搜索相似文档
res = client.search(
    collection_name=collection_name,
    data=query_vector.tolist(),
    filter="subject == 'history'",
    limit=2,
    output_fields=["text", "subject"],
)

# 输出搜索结果
print("Search results:")
for result in res:
    for hit in result:
        print(f"ID: {hit['id']}, Distance: {hit['distance']}, Text: {hit['entity']['text']}")

# # 查询所有符合条件的文档
# res = client.query(
#     collection_name=collection_name,
#     filter="subject == 'history'",
#     output_fields=["text", "subject"],
# )
#
# print("Query results:")
# for doc in res:
#     print(f"Text: {doc['text']}, Subject: {doc['subject']}")

# 删除符合条件的文档
# res = client.delete(
#     collection_name=collection_name,
#     filter="subject == 'history'",
# )
# print(f"Deleted {res} documents.")








