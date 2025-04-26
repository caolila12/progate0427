from fetch_news import fetch_ai_news
from summarize import summarize_text

def main():
    articles = fetch_ai_news()

    for idx, article in enumerate(articles, start=1):
        print(f"\n📰 記事 {idx}")
        print(f"タイトル: {article.get('title')}")
        print(f"要約: {summarize_text(article.get('description') or '')}")
        print(f"URL: {article.get('url')}")
        print(f"公開日時: {article.get('publishedAt')}")

if __name__ == "__main__":
    main()
