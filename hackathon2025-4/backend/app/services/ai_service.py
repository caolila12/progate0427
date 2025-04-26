from typing import Dict, Any
import openai
import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        # OpenAI APIキーを環境変数から読み込む
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    async def summarize_news(self, news: Dict[str, Any]) -> Dict[str, Any]:
        """
        ニュース記事を要約する
        """
        try:
            # OpenAI APIを使用して要約を生成
            response = await openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたはニュース記事を簡潔に要約する専門家です。"},
                    {"role": "user", "content": f"以下のニュース記事を要約してください：\n\nタイトル：{news['title']}\n\n内容：{news['content']}"}
                ]
            )
            
            summary = response.choices[0].message.content
            
            return {
                "original_title": news["title"],
                "summary": summary
            }
        except Exception as e:
            raise Exception(f"要約の生成中にエラーが発生しました: {str(e)}") 