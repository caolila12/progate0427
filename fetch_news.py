import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

# .envファイルからAPIキーを読み込む
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

def fetch_articles(query="生成AI", max_articles=100):
    """
    NewsAPIを使用して指定したキーワードに関連するニュース記事を取得する関数。

    Parameters:
        query (str): 検索キーワード（デフォルトは"生成AI"）。
        max_articles (int): 取得する記事の最大数（デフォルトは100）。

    Returns:
        list: 取得したニュース記事のリスト（タイトルとURLのみ）
    """
    url = "https://newsapi.org/v2/everything"
    headers = {'X-Api-Key': API_KEY}
    params = {
        'q': query,
        'from': from_date,
        'sortBy': 'publishedAt',
        'pageSize': max_articles,
        'language': 'en'  # 必要に応じて言語を変更
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        return [{"title": article["title"], "url": article["url"]} for article in articles]
    else:
        print(f"エラーが発生しました: {response.status_code}")
        return []