import os
import requests
from bs4 import BeautifulSoup
import cohere
import time
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)
API_KEY = os.getenv("COHERE_API_KEY")

# Cohereクライアントをグローバルに設定
cohere_client = None

def init_cohere(api_key=API_KEY):
    global cohere_client
    cohere_client = cohere.Client(api_key)

def get_article_content(url):
    """
    URLから本文を取得する関数
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        article_content = ' '.join([p.get_text() for p in paragraphs])
        return article_content
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def summarize_content(content):
    """
    記事の本文を日本語で要約する関数
    """
    try:
        print("🛠️ summarize_content called!")
        prompt = f"次の英語の文章を日本語で要約してください：\n\n{content}"
        response = cohere_client.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
            k=0,
            p=0.75
        )
        summary = response.generations[0].text.strip()
        return summary
    except Exception as e:
        print(f"Error summarizing content: {e}")
        return None
