import streamlit as st
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# バックエンドのURL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# ページ設定
st.set_page_config(
    page_title="Dashニュース要約",
    page_icon="📰",
    layout="wide"
)

# タイトル
st.title("📰 Dashニュース要約")

# サイドバー
st.sidebar.title("設定")
st.sidebar.info("このアプリは最新のニュースを取得し、AIによって要約します。")

# ニュース一覧の取得
def fetch_news():
    try:
        response = requests.get(f"{BACKEND_URL}/api/news")
        if response.status_code == 200:
            return response.json()["data"]
        else:
            st.error("ニュースの取得に失敗しました。")
            return []
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        return []

# ニュース詳細の取得
def fetch_news_detail(news_id):
    try:
        response = requests.get(f"{BACKEND_URL}/api/news/{news_id}")
        if response.status_code == 200:
            return response.json()["data"]
        else:
            st.error("ニュース詳細の取得に失敗しました。")
            return None
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        return None

# ニュース要約の取得
def fetch_news_summary(news_id):
    try:
        response = requests.get(f"{BACKEND_URL}/api/news/{news_id}/summary")
        if response.status_code == 200:
            return response.json()["data"]
        else:
            st.error("ニュース要約の取得に失敗しました。")
            return None
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        return None

# メインコンテンツ
def main():
    # ニュース一覧の取得
    news_list = fetch_news()
    
    if not news_list:
        st.warning("ニュースが取得できませんでした。")
        return
    
    # ニュース一覧の表示
    for news in news_list:
        with st.expander(f"{news['title']} - {datetime.fromisoformat(news['published_at']).strftime('%Y-%m-%d %H:%M')}"):
            # ニュース詳細の取得
            news_detail = fetch_news_detail(news['id'])
            if news_detail:
                # ソース情報の表示
                st.caption(f"出典: {news_detail.get('source', '不明')}")
                
                # 要約の取得
                summary = fetch_news_summary(news['id'])
                
                if summary:
                    st.subheader("AI要約")
                    st.write(summary['summary'])
                    st.divider()
                
                st.subheader("元の記事")
                st.write(news_detail['content'])
                
                # 元記事へのリンク
                if news_detail.get('url'):
                    st.link_button("元記事を読む", news_detail['url'])

if __name__ == "__main__":
    main() 