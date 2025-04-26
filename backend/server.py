from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.fetch_news import fetch_ai_news
from backend.summarize import summarize_content, get_article_content, init_cohere
from backend.title_rewrite import generate_clickbait_title

app = FastAPI()
init_cohere()

# CORS設定（Streamlitから叩けるようにする）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ニュースリストを取得するAPI
@app.get("/api/news")
def get_news():
    articles = fetch_ai_news(max_articles=5)

    news_data = []
    for idx, article in enumerate(articles):
        title = article['title']
        kajo_title = generate_clickbait_title(title)  # 煽りタイトル
        url = article['url']
        published_at = article['publishedAt']

        # 本文と要約取得（簡易版）
        content = get_article_content(url)
        summary = summarize_content(content) if content else "要約できませんでした"

        news_data.append({
            "id": idx,
            "title": title,
            "kajo_title": kajo_title,
            "summary": summary,
            "url": url,
            "publishedAt": published_at,
            "importance": 80,  # 仮置き。後で速報性スコアなどにできる
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
    content = get_article_content(url)
    summary = summarize_content(content) if content else "要約できませんでした"
    return {"data": {"summary": summary}}
