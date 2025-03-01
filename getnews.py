import tushare as ts
import pandas as pd
from openai import OpenAI
from datetime import datetime,timedelta
import pymongo
import json
import logging
from dotenv import load_dotenv 
import os

# 加载 .env 文件
load_dotenv()


# 获取 Tushare Token
tushare_token = os.getenv("TUSHARE_TOKEN")
# 获取api_key
api_key = os.getenv("DEEPSEEK_API_KEY")
# 获取AI URL
ai_url = os.getenv("OPENAI_BASE_URL")
# 设置 Tushare Token
ts.set_token(tushare_token)
# 获取数据库连接字符串
mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongo:27017/')

# 初始化 pro API 客户端
pro = ts.pro_api()

# 配置AI的api和url
client = OpenAI(
    api_key = api_key,
    base_url = ai_url)

# 获取新浪财经新闻
def get_news(news_site):
    """自动获取过去 3 小时的新闻"""
    now = datetime.now()
    past_3h = now - timedelta(hours=3)  # 获取当前时间的3小时前
    
    start = past_3h.strftime("%Y-%m-%d %H:%M:%S")  # 过去3小时的开始时间
    end = now.strftime("%Y-%m-%d %H:%M:%S")  # 当前时间
    
    df = pro.news(src=news_site, start_date=start, end_date=end, page=1, page_size=10)
    # 确保将 title 和 content 转换为字符串，并处理缺失值
    df['title'] = df['title'].fillna('').astype(str)
    df['content'] = df['content'].fillna('').astype(str)
    # 合并标题和内容，作为模型输入
    news_content = "\n".join(df['title'] + "\n" + df['content'])
    return news_content
# AI分析新闻
def analysis_news(news_centent):
    try:
        # 构造 Deepseek 提示词
        prompt = f"""
你是一个经验丰富的财经专家，专注于全球市场和经济动态。以下是过去3小时内的财经新闻，请你根据新闻内容自动识别新闻涉及的行业，并分析其对A股上市公司和概念板块的影响。

## Profile
- language: 中文
- description: 专注于全球市场和经济动态的财经专家，擅长分析财经新闻对A股上市公司和概念板块的影响。
- background: 拥有多年财经分析经验，熟悉全球市场动态和A股市场。
- personality: 严谨、细致、逻辑性强。
- expertise: 财经新闻分析、行业影响评估、A股市场研究。
- target_audience: 投资者、财经分析师、A股市场参与者。

## Skills

1. **核心技能类别**
   - **行业识别**: 根据新闻内容快速识别涉及的行业。
   - **行业分析**: 使用特定行业的分析框架进行深入分析。
   - **影响评估**: 评估新闻对A股上市公司和概念板块的影响。
   - **报告撰写**: 撰写详细的分析报告，包括受影响的公司和板块。

2. **辅助技能类别**
   - **数据收集**: 收集和整理相关财经新闻和数据。
   - **市场研究**: 研究A股市场的动态和趋势。
   - **政策解读**: 解读相关政策对行业的影响。
   - **沟通能力**: 与投资者和分析师进行有效沟通。

## Rules

1. **基本原则**
   - **准确性**: 确保分析的准确性和可靠性。
   - **及时性**: 在新闻发布后尽快进行分析。
   - **客观性**: 保持客观，不带有个人偏见。
   - **全面性**: 全面考虑新闻对行业和市场的多方面影响。

2. **行为准则**
   - **保密性**: 保护客户和公司的机密信息。
   - **专业性**: 保持专业态度，遵守职业道德。
   - **透明度**: 在分析报告中明确说明分析方法和依据。
   - **责任感**: 对分析结果负责，及时更新和修正。

3. **限制条件**
   - **信息来源**: 仅使用可靠和权威的财经新闻来源。
   - **时间限制**: 在新闻发布后3小时内完成分析。
   - **范围限制**: 仅分析对A股上市公司和概念板块的影响。
   - **法律合规**: 遵守相关法律法规，不进行非法操作。

## Workflows

- 目标: 分析过去3小时内的财经新闻对A股上市公司和概念板块的影响。
- 步骤 1: 自动选择行业，根据新闻内容判断涉及的主要行业。
- 步骤 2: 使用相应的行业分析框架进行深入分析。
- 步骤 3: 列出受影响的公司和板块，分析是利好还是利空，并简要解释原因。
- 预期结果: 提供详细的分析报告，帮助投资者和市场参与者做出决策。

3. **新闻内容**：
    - 以下是新闻内容，请分析并提炼出对A股相关公司和板块的影响。

    {news_centent}

4. **输出符合以下结构的纯json格式的结果,方便程序直接存入数据库**

    - **新闻标题**：[标题]
    - **行业分析框架**：[选择的行业]
    
    - **相关上市公司**：
        - [公司名称+股票代码]：利好/利空，分析原因。
        
    - **相关概念板块**：
        - [概念板块名称]：利好/利空，分析原因。


        """
        response = client.chat.completions.create(
            model="ep-20250217151011-nmg5k",
            messages=[{"role": "user", "content": prompt}]
        )
        
         # 确保返回的是单个 JSON 对象
        response_content = response.choices[0].message.content.strip()
        logging.info(f"AI 分析结果: {response_content}")
                # 尝试解析返回内容为 JSON 字典
        return response_content

    
    except Exception as e:
        logging.error(f"AI 分析生成失败: {str(e)}")
        return f"AI 分析生成失败: {str(e)}"


# 存储数据
def store_news_analysis(news_data):
    try:

        # 连接到 MongoDB
        client = pymongo.MongoClient(mongo_uri)
        db = client["financial_news_db"]
        collection = db["news_analysis"]
        # 获取当前时间戳
        current_timestamp = datetime.now()
            
        # 拆分数据并插入MongoDB
        for news_item in news_data:
            # 为每个新闻条目添加当前时间戳
            news_item["timestamp"] = current_timestamp
    
            # 插入到MongoDB
            collection.insert_one(news_item)
        print("数据已成功插入到MongoDB！")
        
    except Exception as e:
        print(f"插入数据库时出错: {e}")


# 查询数据
def get_latest_news():
    try:
        # 连接到 MongoDB
        client = pymongo.MongoClient(mongo_uri)
        db = client["financial_news_db"]
        collection = db["news_analysis"]

        # 获取按时间戳降序排序的前10条新闻
        latest_news = collection.find().sort("timestamp", pymongo.DESCENDING).limit(30)

        # 将结果转化为列表（可根据需要处理格式）
        news_list = list(latest_news)

        return news_list

    except Exception as e:
        print(f"获取数据时出错: {e}")
        return []
    

def main():
    #定义新闻源
    # sina=新浪；10jqka=同花顺；wallstreetcn=华尔街；eastmoney=东方财富
    news_site = "10jqka"
    # 获取新闻
    news = get_news(news_site)
    print(news)
    print("-------------------")
    # AI分析
    analysis_result = analysis_news(news)
    print(analysis_result)
    print("-------------------")
    # 去掉"```json", "" 和空格
    analysis_result = analysis_result.replace("```json", "").replace("```", "").strip()
    print(analysis_result)
    print("-------------------")
    # 把文本字符转成python字典
    data = json.loads(analysis_result)
    # 确保 data 是列表格式
    if isinstance(data, dict):
        data = [data]  # 如果是单条数据，转换成列表
    print(data)
    # 把数据存入数据     
    store_news_analysis(data)   

if __name__ == "__main__":
    main()