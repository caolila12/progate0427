from fetch_news import fetch_articles
from summarize import init_cohere, get_article_content, summarize_content
import time
from datetime import datetime

#日付表示変換
def format_published_date(published_at_str):
    """
    ISO形式の日付文字列を「YYYY年M月D日」形式に整形する関数
    """
    try:
        dt = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%SZ")
        return f"{dt.year}年{dt.month}月{dt.day}日"
    except Exception as e:
        print(f"日付変換エラー: {e}")
        return published_at_str  # エラー時はそのまま返す


def main():
    init_cohere()

    articles = fetch_articles()

    for idx, article in enumerate(articles, start=1):
        print(f"\n📰 記事 {idx}")
        print(f"タイトル: {article['title']}")
        print(f"公開日時: {format_published_date(article['publishedAt'])}")
        print(f"URL: {article['url']}")

        content = get_article_content(article['url'])
        if content:
            summary = summarize_content(content)
            if summary:
                print(f"要約: {summary}\n")
            else:
                print("要約に失敗しました。")
        else:
            print("記事本文の取得に失敗しました。")

        time.sleep(1)  # APIへの負荷軽減のため1秒待つ

if __name__ == "__main__":
    main()
