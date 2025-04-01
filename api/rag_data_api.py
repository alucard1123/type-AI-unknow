from flask import Blueprint, jsonify, request

from project.type_AI_unknow.rag.milvus_tool import save_docx_to_milvus, serch_data_from_milvus
from project.type_AI_unknow.rag.model_tool import rag_query

# 创建一个蓝图对象
api_bp = Blueprint('api', __name__, url_prefix='/api')

# 示例 API 路由
@api_bp.route('/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, this is an API endpoint!")

@api_bp.route('/greet/<name>', methods=['GET'])
def greet(name):
    return jsonify(message=f"Hello, {name}!")

@api_bp.route('/submit', methods=['POST'])
def submit():
    data = request.json  # 获取 JSON 数据
    name = data.get('name', 'Guest')
    return jsonify(message=f"Hello, {name}!")

@api_bp.route('/load_file', methods=['POST'])
def load_file():
    # 检查请求中是否包含文件
    if 'file' not in request.files:
        return jsonify(error="No file part in the request"), 400

    file = request.files['file']

    # 检查文件是否为空
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    # 检查文件是否为 .docx 格式
    if not file.filename.endswith('.docx'):
        return jsonify(error="File format not supported. Only .docx files are allowed."), 400

    # try:
    # # 将文件内容读取到内存中，并包装为 BytesIO 对象
    # file_stream = io.BytesIO(file.read())
    # # 使用 python-docx 提取 .docx 文件中的文本内容
    # doc = Document(file_stream)
    # text_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    # # 调用 save_data_to_milvus 方法，传递文本内容
    # result = save_data_to_milvus(text_content)

    # # 保存文件到指定路径（可以根据需要修改）
    file_path=f'./data/{file.filename}'
    # file_path = f"./uploads/{file.filename}"
    # file.save(file_path)
    save_docx_to_milvus(file_path)

    # 返回成功响应
    return jsonify(message="File uploaded successfully"), 200
    # except Exception as e:
    #     # 捕获异常并返回错误信息
    #     return jsonify(error=f"An error occurred: {str(e)}"), 500


@api_bp.route('/search_data', methods=['GET'])
def search_data():
    data = request.args
    query = data.get('query')
    final_result = []
    for result in serch_data_from_milvus(query):
        for hit in result:
            final_result.append(f"ID: {hit['id']}, Distance: {hit['distance']}, Text: {hit['entity']['text']}")
    return jsonify(final_result)


@api_bp.route('/rag_search', methods=['GET'])
def rag_search():
    data = request.args
    query = data.get('query')
    result = rag_query(query).content
    return jsonify(result)