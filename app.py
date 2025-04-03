import os

from flask import Flask
from langchain_community.chat_models import ChatTongyi
from langchain_community.llms.ollama import Ollama
from pymilvus import MilvusClient
from pymilvus import connections

from project.type_AI_unknow.api import api_bp

app = Flask(__name__)

# 加载配件信息
app.config.from_pyfile('./settings.cfg')

# 注册 api 蓝图
app.register_blueprint(api_bp)


app.config['MILVUS_CLIENT'] = MilvusClient(uri=app.config.get('MILVUS_URL'),
                    token=app.config.get('MILVUS_TOKEN'))
os.environ["DASHSCOPE_API_KEY"] = app.config.get('API_KEY')
# app.config['CHAT_LLM'] = ChatTongyi(streaming=True, model='deepseek-r1-distill-qwen-32b')
app.config['CHAT_LLM'] =  Ollama(model="deepseek-r1:8b")





if __name__ == '__main__':
    app.run(debug=True)
