import streamlit as st
import requests
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime, timedelta

today = datetime.today().date()

# バックエンドのURL
BACKEND_URL = "http://localhost:8000"

# ページ設定
st.set_page_config(
    page_title="NewsDash",
    page_icon="📰",
    layout="wide"
)

# セッション状態の初期化
if 'is_kajo_mode' not in st.session_state:
    st.session_state.is_kajo_mode = False

# タイトル
st.title("📰 News Dash")

# サイドバー
st.sidebar.title("検索条件")
st.sidebar.info("このアプリは最新のニュースを取得し、AIによって要約します。")

# サイドバーでクエリ入力
query = st.sidebar.text_input(
    "ニュースを検索するキーワードを入力してください",
    value="生成AI" #デフォルト
)

# サイドバーで開始日入力
start_date = st.sidebar.date_input(
    "検索開始日を指定してください（30日前まで指定できます）",
    value=today - timedelta(days=7),
    min_value=today - timedelta(days=30),
    max_value=today
)

# サイドバーで終了日入力
end_date = st.sidebar.date_input(
    "検索終了日",
    value=today,
    min_value=start_date,
    max_value=today
)

sort_option = st.sidebar.selectbox(
    "並び替え方法を選んでください",
    ("Dash度順", "新着順")
)


def set_dark_mode():
    dark_css = """
    <style>
    /* メインエリア（stApp）だけダークモード */
    .stApp {
        background-color: #111;
        color: #f5f5f5;
    }

    /* 本文中の通常テキストは白 */
    .stApp p, .stApp div, .stApp span, .stApp label {
        color: #f5f5f5 !important;
    }

    /* タイトルだけ赤色 */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #ff4b4b !important;
    }

    /* サイドバー部分だけ白背景・黒文字 */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        color: #000000;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #000000 !important;
    }
    </style>
    """
    st.markdown(dark_css, unsafe_allow_html=True)







# かじょふわモードの切り替え
st.session_state.is_kajo_mode = st.toggle(
    "かじょふわモード",
    value=st.session_state.is_kajo_mode,
    help="かじょふわモードをオンにすると、タイトルがかじょふわバージョンに変わります"
)

if st.session_state.is_kajo_mode:
    set_dark_mode()

# ニュースデータを取得する関数
def fetch_news(query="生成AI", from_date=None, to_date=None) -> List[Dict[str, Any]]:
    try:

        params = {"query": query}
        if from_date:
            params["from_date"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            params["to_date"] = to_date.strftime("%Y-%m-%d")


        response = requests.get(f"{BACKEND_URL}/api/news", params=params)
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

         # 投稿日時（日本語フォーマット）
        published_at = news_item.get('publishedAt', '')
        if published_at:
            try:
                dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                published_at_jp = f"{dt.year}年{dt.month}月{dt.day}日"
                st.caption(f"🕒 更新日時: {published_at_jp}")
            except Exception as e:
                st.caption(f"🕒 更新日時: {published_at}")
        
        # 要約
        st.markdown(news_item.get('summary', ''))
        
        # 重要度
        importance = news_item.get('importance', 0)
        st.progress(importance / 100, text=f"Dash度: {importance}%")
        
        # 元の記事へのリンク
        url = news_item.get('url', '')
        st.markdown(f"[元の記事を読む]({url})")

# ニュースデータの取得と表示
news_data = fetch_news(query=query, from_date=start_date, to_date=end_date)
st.write(f"取得したニュース数: {len(news_data)} 件")

# 🧹 ここでソート！
if sort_option == "Dash度順":
    news_data = sorted(news_data, key=lambda x: x.get('importance', 0), reverse=True)
elif sort_option == "新着順":
    news_data = sorted(news_data, key=lambda x: x.get('publishedAt', ""), reverse=True)

if news_data:
    for news_item in news_data[:10]:
        display_news_card(news_item)
else:
    st.info("ニュースを読み込み中...")

if __name__ == "__main__":
    pass 