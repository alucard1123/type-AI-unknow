# 使用官方的 Python 3.11 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到容器的 /app 目录中
COPY . /app

# 创建一个目录用于挂载模型
RUN mkdir -p /app/models


# 安装依赖项（包括 Gunicorn 和 ping 工具）
RUN apt-get update && \
    apt-get install -y --no-install-recommends iputils-ping && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt gunicorn && \
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# 暴露 Flask 应用运行的端口（默认是 5000）
EXPOSE 5000

# 使用 Gunicorn 启动应用
# CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "app:app"]

# 启动 Flask 应用
CMD ["python", "app.py"]