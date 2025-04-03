from flask import current_app
from project.type_AI_unknow.rag.milvus_tool import serch_data_from_milvus


# 构造提示词（Prompt）
def create_prompt(query, context_docs):
    # 将检索到的文档拼接成上下文
    context = "\n".join(context_docs)
    prompt = f"""
    根据以下上下文回答问题：
    上下文：
    {context}

    问题：
    {query}

    回答：
    """
    return prompt.strip()


def rag_query(query):
    # 从milvus向量库查询最符合的数据
    data = serch_data_from_milvus(query)
    # 格式化查询的文档格式
    retrieved_docs = [hit.get('entity').get('text') for result in data for hit in result]
    # 构造提示词
    prompt = create_prompt(query, retrieved_docs)
    # 调用大模型生成回答
    chatLLM = current_app.config.get('CHAT_LLM')
    response = chatLLM.invoke(prompt)
    print(response)
    return response