from flask import Flask, render_template, jsonify
import pymongo
from datetime import datetime
from getnews import get_latest_news

app = Flask(__name__)

# 连接到 MongoDB 数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["financial_news_db"]
collection = db["news_analysis"]

# 时间戳格式化函数
def format_timestamp(timestamp):
    if isinstance(timestamp, datetime):
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')
    return timestamp

@app.route('/')
def index():
    # 获取最新的新闻
    latest_news = get_latest_news()
    
    # 打印新闻数据，检查数据是否正确
    print("获取到的新闻数据：", latest_news)
    
    # 格式化每条新闻的时间戳
    for item in latest_news:
        item['timestamp'] = format_timestamp(item['timestamp'])
    
    # 如果没有新闻数据，返回一个空列表
    if not latest_news:
        print("没有获取到新闻数据！")
    
    # 将新闻数据传递给模板进行渲染
    return render_template('index.html', news=latest_news)

@app.route('/latest-news')
def latest_news():
    news = get_latest_news()
    
    # 格式化每条新闻的时间戳
    for item in news:
        item['timestamp'] = format_timestamp(item['timestamp'])
    
    # 返回 JSON 格式的新闻数据
    return jsonify(news)

if __name__ == '__main__':
    #app.run(debug=True, host="0.0.0.0", port=5000)
    app.run(debug=True)