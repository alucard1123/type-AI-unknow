import os

from flask import Flask
from langchain_community.chat_models import ChatTongyi
from pymilvus import MilvusClient
from pymilvus import connections

from project.type_AI_unknow.api import api_bp

app = Flask(__name__)

# 加载配件信息
app.config.from_pyfile('./settings.cfg')

# 注册 api 蓝图
app.register_blueprint(api_bp)
# 建立 Milvus 连接

# 将连接对象存入配置中，后续可用 connections.get_connection("default") 获取连接
# app.config['MILVUS_CLIENT'] = connections.connect(alias="default",
#                     uri=app.config.get('MILVUS_URL'),
#                     token=app.config.get('MILVUS_TOKEN'))

app.config['MILVUS_CLIENT'] = MilvusClient(uri=app.config.get('MILVUS_URL'),
                    token=app.config.get('MILVUS_TOKEN'))
os.environ["DASHSCOPE_API_KEY"] = app.config.get('API_KEY')
app.config['CHAT_LLM'] = ChatTongyi(streaming=True, model='deepseek-r1-distill-qwen-32b')


# 配置静态文件和模板文件夹
# app.static_folder = 'static'
# app.template_folder = 'templates'



if __name__ == '__main__':
    app.run(debug=True)
