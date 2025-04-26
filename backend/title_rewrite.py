import os
import google.generativeai as genai
from dotenv import load_dotenv

# .envファイルからGeminiのAPIキーを読み込み
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Geminiのクライアントを初期化
genai.configure(api_key=GEMINI_API_KEY)

def generate_clickbait_title(original_title):
    """
    元のニュースタイトルを、より衝撃的で目を引く煽りタイトルに変換する関数（Gemini版）
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
以下のニュースタイトルを、より衝撃的で目を引く日本語タイトルに【1つだけ】変換してください。
タイトル以外の文章（案内、説明文、注意書きなど）は絶対に書かないでください。
【元のタイトル】{original_title}
【新しいタイトル】"""

        response = model.generate_content(prompt)

        # レスポンスからテキストを取り出し、きれいに整形
        if response and response.text:
            new_title = response.text.strip()
            return new_title
        else:
            print("レスポンスが空です")
            return original_title

    except Exception as e:
        print(f"煽りタイトル生成エラー（Gemini版）: {e}")
        return original_title
