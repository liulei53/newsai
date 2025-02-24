# 使用官方 Python 作为基础镜像
FROM python:3.9-slim

# 安装 cron
RUN apt-get update && apt-get install -y cron

# 设置工作目录
WORKDIR /app

# 将本地项目复制到容器中
COPY . /app

# 安装项目的依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装 pymongo
RUN pip install pymongo

# 添加定时任务：每 3 小时运行一次 getnews.py
RUN echo "0 */3 * * * python /app/getnews.py" > /etc/cron.d/getnews-cron

# 给 cron 文件添加执行权限
RUN chmod 0644 /etc/cron.d/getnews-cron

# 创建日志文件，cron 将把输出写入其中
RUN touch /var/log/cron.log

# 启动 cron 服务和 Flask 应用
CMD cron && tail -f /var/log/cron.log & python app.py

# 映射容器的端口到宿主机的 5001 端口
EXPOSE 5000
