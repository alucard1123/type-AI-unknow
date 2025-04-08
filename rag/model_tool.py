from flask import current_app
from project.type_AI_unknow.rag.milvus_tool import search_data_from_milvus


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


def create_testcase_prompt(query, context_docs):
    # 将 PRD 文档内容合并成一段
    prd_context = "\n".join(context_docs)

    # 定义一个测试用例的模板格式
    prompt = f"""
    根据以下 PRD 文档和用户故事生成一个规范化的测试用例。请严格按照以下格式输出测试用例：

    测试用例格式：
    ------------------------------
    测试用例标题: [在此填写测试用例标题]
    前置条件: [在此填写前置条件]
    测试步骤:
      1. [步骤 1]
      2. [步骤 2]
      3. [步骤 3]
      ...
    预期结果: [在此填写预期结果]
    ------------------------------

    PRD 文档：
    {prd_context}

    用户故事：
    {query}

    回答：
    """
    return prompt.strip()


def rag_query(query):
    # 从milvus向量库查询最符合的数据
    data = search_data_from_milvus(query)
    # 格式化查询的文档格式
    retrieved_docs = [hit.get('entity').get('text') for result in data for hit in result]
    # 构造提示词
    prompt = create_prompt(query, retrieved_docs)
    # 调用大模型生成回答
    chatLLM = current_app.config.get('CHAT_LLM')
    response = chatLLM.invoke(prompt)
    print(response)
    return response

def testcase_query(query,docx_name):
    # 从milvus向量库查询最符合的数据
    data = search_data_from_milvus(query_data=None,filter=f"subject == '{docx_name}'",limit=None)
    # 格式化查询的文档格式
    retrieved_docs = [result.get('text') for result in data ]
    # 构造提示词
    prompt = create_testcase_prompt(query, retrieved_docs)
    # 调用大模型生成回答
    chatLLM = current_app.config.get('CHAT_LLM')
    response = chatLLM.invoke(prompt)
    print(response)
    return response