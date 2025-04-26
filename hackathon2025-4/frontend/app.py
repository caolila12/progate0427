import streamlit as st
import requests
import pandas as pd
from typing import List, Dict, Any

# バックエンドのURL
BACKEND_URL = "http://localhost:8000"

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
        response = requests.get(f"{BACKEND_URL}/api/news")
        response.raise_for_status()
        return response.json()["data"]
    except Exception as e:
        st.error(f"ニュースの取得に失敗しました: {str(e)}")
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