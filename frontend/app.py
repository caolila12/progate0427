import streamlit as st
import requests
import pandas as pd
from typing import List, Dict, Any
# backendから直接関数をimportする
from backend.fetch_news import fetch_ai_news
from backend.summarize import summarize_content, get_article_content
from backend.title_rewrite import generate_clickbait_title


# バックエンドのURL
#BACKEND_URL = "http://localhost:8000"

# ページ設定
st.set_page_config(
    page_title="ニュースアプリ",
    page_icon="📰",
    layout="wide"
)

# セッション状態の初期化
if 'is_kajo_mode' not in st.session_state:
    st.session_state.is_kajo_mode = False

# タイトル
st.title("📰 最新ニュース")

# サイドバー
st.sidebar.title("設定")
st.sidebar.info("このアプリは最新のニュースを取得し、AIによって要約します。")

# かじょふわモードの切り替え
st.session_state.is_kajo_mode = st.toggle(
    "かじょふわモード",
    value=st.session_state.is_kajo_mode,
    help="かじょふわモードをオンにすると、タイトルがかじょふわバージョンに変わります"
)

# ニュースデータを取得する関数
def fetch_news() -> List[Dict[str, Any]]:
    try:
        articles = fetch_ai_news(max_articles=5)

        news_data = []
        for idx, article in enumerate(articles):
            title = article['title']
            kajo_title = generate_clickbait_title(title)
            url = article['url']
            published_at = article['publishedAt']

            content = get_article_content(url)
            summary = summarize_content(content) if content else "要約できませんでした"

            news_data.append({
                "id": idx,
                "title": title,
                "kajo_title": kajo_title,
                "summary": summary,
                "url": url,
                "publishedAt": published_at,
                "importance": 80,
            })

        return news_data

    except Exception as e:
        st.error(f"ニュースの取得に失敗しました: {str(e)}")
        return []




# ニュースカードを表示する関数
def display_news_card(news_item: Dict[str, Any]):
    with st.container():
        st.markdown("---")
        # タイトル
        title = news_item.get('kajo_title') if st.session_state.is_kajo_mode else news_item.get('title')
        st.markdown(f"### {title}")
        
        # 要約
        st.markdown(news_item.get('summary', ''))
        
        # 重要度
        importance = news_item.get('importance', 0)
        st.progress(importance / 100, text=f"重要度: {importance}%")
        
        # 元の記事へのリンク
        url = news_item.get('url', '')
        st.markdown(f"[元の記事を読む]({url})")

# ニュースデータの取得と表示
news_data = fetch_news()

if news_data:
    for news_item in news_data:
        display_news_card(news_item)
else:
    st.info("ニュースを読み込み中...")

if __name__ == "__main__":
    pass 