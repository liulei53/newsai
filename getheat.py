import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


import time
# 获取网页内容
url = 'https://gushitong.baidu.com/hotlist?activeTab=0&market=ab'  # 这里填入网页的 URL
response = requests.get(url)

# 检查是否请求成功
if response.status_code == 200:
    html = response.text
    
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # 使用 CSS 选择器提取 `40.8w` 热度数据
    hot_item = soup.find('div', class_='right-item hot')  # 找到包含热度数据的 div
    if hot_item:
        hot_value = hot_item.find('span').text.strip()  # 提取里面的热度数值
        print(f"热度数据：{hot_value}")  # 输出热度数据
    else:
        print("没有找到热度数据")
else:
    print(f"请求失败，状态码：{response.status_code}")