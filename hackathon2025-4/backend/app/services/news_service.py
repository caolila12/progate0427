import requests
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class NewsService:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"
        if not self.api_key:
            raise ValueError("NEWS_API_KEY is not set in environment variables")

    async def get_latest_news(self) -> List[Dict[str, Any]]:
        """
        最新のニュースを取得する
        """
        try:
            # 過去24時間のニュースを取得
            from_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            
            # NewsAPIを使用してニュースを取得
            response = requests.get(
                f"{self.base_url}/everything",
                params={
                    "q": "日本",  # 日本のニュースを検索
                    "language": "ja",  # 日本語のニュース
                    "sortBy": "publishedAt",  # 公開日時でソート
                    "from": from_date,  # 過去24時間
                    "apiKey": self.api_key
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"NewsAPI request failed: {response.text}")
            
            data = response.json()
            
            # レスポンスを整形
            news_list = []
            for article in data.get("articles", [])[:10]:  # 最新10件を取得
                news_list.append({
                    "id": article.get("url", ""),  # URLをIDとして使用
                    "title": article.get("title", ""),
                    "content": article.get("description", ""),
                    "published_at": article.get("publishedAt", ""),
                    "source": article.get("source", {}).get("name", ""),
                    "url": article.get("url", "")
                })
            
            return news_list
            
        except Exception as e:
            raise Exception(f"ニュースの取得中にエラーが発生しました: {str(e)}")

    async def get_news_by_id(self, news_id: str) -> Dict[str, Any]:
        """
        特定のニュース記事を取得する
        """
        try:
            # NewsAPIを使用して特定の記事を取得
            response = requests.get(
                f"{self.base_url}/everything",
                params={
                    "q": news_id,  # URLを検索クエリとして使用
                    "language": "ja",
                    "apiKey": self.api_key
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"NewsAPI request failed: {response.text}")
            
            data = response.json()
            articles = data.get("articles", [])
            
            if not articles:
                raise Exception("Article not found")
            
            article = articles[0]  # 最初の記事を使用
            
            return {
                "id": article.get("url", ""),
                "title": article.get("title", ""),
                "content": article.get("content", article.get("description", "")),
                "published_at": article.get("publishedAt", ""),
                "source": article.get("source", {}).get("name", ""),
                "url": article.get("url", "")
            }
            
        except Exception as e:
            raise Exception(f"ニュースの取得中にエラーが発生しました: {str(e)}") 