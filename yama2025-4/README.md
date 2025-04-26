# ニュース要約アプリ

FastAPIとStreamlitを使用したニュース要約アプリケーションです。

## 機能

- 最新ニュースの取得
- AIによるニュース要約
- レスポンシブなUI

## セットアップ

### バックエンド

1. バックエンドディレクトリに移動
```bash
cd backend
```

2. 仮想環境の作成と有効化
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

4. 環境変数の設定
`.env`ファイルを作成し、以下の内容を設定：
```
OPENAI_API_KEY=your_openai_api_key
NEWS_API_KEY=your_news_api_key
```

5. バックエンドの起動
```bash
uvicorn app.main:app --reload
```

### フロントエンド

1. フロントエンドディレクトリに移動
```bash
cd frontend
```

2. 仮想環境の作成と有効化
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

4. 環境変数の設定
`.env`ファイルを作成し、以下の内容を設定：
```
BACKEND_URL=http://localhost:8000
```

5. フロントエンドの起動
```bash
streamlit run app.py
```

## 使用方法

1. ブラウザで http://localhost:8501 にアクセス
2. ニュース一覧が表示されます
3. 各ニュースをクリックして詳細と要約を表示

## 技術スタック

- バックエンド: FastAPI
- フロントエンド: Streamlit
- AI: OpenAI GPT-3.5
- ニュースAPI: 未定（実装時に選択） 