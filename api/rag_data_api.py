from flask import Blueprint, jsonify, request

from project.type_AI_unknow.rag.milvus_tool import save_docx_to_milvus, search_data_from_milvus
from project.type_AI_unknow.rag.model_tool import rag_query, testcase_query

# 创建一个蓝图对象
api_bp = Blueprint('api', __name__, url_prefix='/api')

# 上传数据到向量库
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

    # # 保存文件到指定路径（可以根据需要修改）
    filename = file.filename
    file_path=f'./data/{filename}'
    file.save(file_path)
    save_docx_to_milvus(file_path,'.'.join(filename.split('.')[:-1]))
    # 返回成功响应
    return jsonify(message="File uploaded successfully"), 200

# 从向量库查询数据
@api_bp.route('/search_data', methods=['GET'])
def search_data():
    data = request.args
    query = data.get('query')
    final_result = []
    for result in search_data_from_milvus(query):
        for hit in result:
            final_result.append(f"ID: {hit['id']}, Distance: {hit['distance']}, Text: {hit['entity']['text']}")
    return jsonify(final_result)

# 使用rag查询数据
@api_bp.route('/rag_search', methods=['GET'])
def rag_search():
    data = request.args
    query = data.get('query')
    result = rag_query(query)
    return jsonify(result)


@api_bp.route('/rag_testcase', methods=['GET'])
def rag_testcase():
    data = request.args
    query = data.get('query')
    docx_name = data.get('docx_name')
    result = testcase_query(query,docx_name)
    return jsonify(result)