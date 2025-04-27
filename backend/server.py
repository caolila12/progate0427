from fastapi import FastAPI, Query
from typing import Optional
from datetime import date
from fastapi.middleware.cors import CORSMiddleware
from backend.fetch_news import fetch_ai_news
from backend.summarize import summarize_content, get_article_content, init_cohere
from backend.title_rewrite import generate_clickbait_title

app = FastAPI()
init_cohere()
summary_cache = {}

# CORS設定（Streamlitから叩けるようにする）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ニュースリストを取得するAPI
@app.get("/api/news")
def get_news(query: str = "生成AI", from_date: Optional[date] = None, to_date: Optional[date] = None):
    articles = fetch_ai_news(query=query, max_articles=10, from_date=from_date, to_date=to_date)

    news_data = []
    for idx, article in enumerate(articles):
        title = article['title']
        kajo_title = generate_clickbait_title(title)  # 煽りタイトル
        url = article['url']
        published_at = article['publishedAt']
        importance = article.get('importance', 80)

        # ✅ 本文と要約取得（キャッシュ確認付き！）
        if url in summary_cache:
            summary = summary_cache[url]
        else:
            content = get_article_content(url)
            summary = summarize_content(content) if content else "要約できませんでした"
            summary_cache[url] = summary  # キャッシュ保存

        news_data.append({
            "id": idx,
            "title": title,
            "kajo_title": kajo_title,
            "summary": summary,
            "url": url,
            "publishedAt": published_at,
            "importance": importance,
        })

    return {"data": news_data}


# 個別ニュース詳細取得
@app.get("/api/news/{news_id}")
def get_news_detail(news_id: int):
    articles = fetch_ai_news(max_articles=5)
    article = articles[news_id]
    url = article['url']
    content = get_article_content(url)
    return {"data": {"content": content}}

# 個別ニュース要約取得
@app.get("/api/news/{news_id}/summary")
def get_news_summary(news_id: int):
    articles = fetch_ai_news(max_articles=5)
    article = articles[news_id]
    url = article['url']
    # 要約キャッシュを確認
    if url in summary_cache:
        summary = summary_cache[url]
    else:
        content = get_article_content(url)
        summary = summarize_content(content) if content else "要約できませんでした"
        summary_cache[url] = summary  # キャッシュ保存

    return {"data": {"summary": summary}}
