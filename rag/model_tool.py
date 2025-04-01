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
    # 用户输入的问题
    # query = "尽净露天机。只恐时人自执迷是那首诗里面的"

    data = serch_data_from_milvus(query)
    print(data)

    retrieved_docs = [hit.get('entity').get('text') for result in data for hit in result]
    print(retrieved_docs)

    # 构造提示词
    prompt = create_prompt(query, retrieved_docs)

    chatLLM = current_app.config.get('CHAT_LLM')

    # 调用大模型生成回答
    response = chatLLM.invoke(prompt)

    # 输出结果
    print("模型的回答：", response)

    return response