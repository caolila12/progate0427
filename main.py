from fetch_news import fetch_articles
from summarize import init_cohere, get_article_content, summarize_content
import time

def main():
    init_cohere()

    articles = fetch_articles()

    for idx, article in enumerate(articles, start=1):
        print(f"\n📰 記事 {idx}")
        print(f"タイトル: {article['title']}")
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
