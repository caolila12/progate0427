import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, date
from typing import Optional

#from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
# .envファイルからAPIキーを読み込む
load_dotenv(dotenv_path)
API_KEY = os.getenv("NEWS_API_KEY")

def fetch_ai_news(query="生成AI", from_date: Optional[date] = None, to_date: Optional[date] = None, max_articles=10):
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
        'sortBy': 'publishedAt',
        'pageSize': max_articles,
        'language': 'en'  # 必要に応じて言語を変更
    }

    if from_date:
        params['from'] = from_date.strftime("%Y-%m-%d")

    if to_date:
        params['to'] = to_date.strftime("%Y-%m-%d")

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        today = datetime.today().date()

        news_list = []
        for article in articles:
            title = article.get("title", "")
            url = article.get("url", "")
            publishedAt_str = article.get("publishedAt", "")

            # publishedAtを日付型に変換
            try:
                published_date = datetime.strptime(publishedAt_str, "%Y-%m-%dT%H:%M:%SZ").date()
            except:
                published_date = today  # パース失敗したら今日

            # ① 新しさスコア（最大10点）
            days_ago = (today - published_date).days
            freshness_score = max(0, 10 - days_ago)

            # ② キーワードスコア（最大90点）
            high_impact_keywords = ["世界初", "革命", "革新", "画期的", "新時代", "新", "ブレイクスルー", "次世代", "新時代", "初", "歴史的", "驚愕", "再定義", "大発見", "常識を覆す", "未踏", "ゼロから", "驚異の", "全く新しい", "想像を超える", "飛躍的進歩"]
            normal_impact_keywords = ["生成AI", "ディープラーニング", "新技術", "機械学習", "自動運転", "医療AI", "拡張現実", "仮想現実", "量子コンピュータ", "最先端", "注目", "強化", "進化", "発展", "実用化", "研究開発", "イノベーション", "グローバル展開", "特許取得", "資金調達", "プラットフォーム拡張"]
            boost_score = 0
            for keyword in high_impact_keywords:
                if keyword in title:
                    boost_score += 30
            for keyword in normal_impact_keywords:
                if keyword in title:
                    boost_score += 15

            # ③ 最終スコア
            importance = freshness_score + boost_score
            importance = min(100, importance)

            news_list.append({
                "title": title,
                "url": url,
                "publishedAt": publishedAt_str,
                "importance": importance
            })

        return news_list

    else:
        print(f"エラーが発生しました: {response.status_code}")
        return []