# Expense Agent - AI仕訳自動化エージェント

Google ADK × Gemini を活用した経費精算の仕訳自動化エージェント。

## セットアップ

### 前提条件

- Python 3.12
- Gemini APIキー（https://aistudio.google.com/apikey で取得）

### 環境構築
```bash
cd expense-agent

# 仮想環境の作成と有効化（Git Bash）
python -m venv .venv
source .venv/Scripts/activate

# パッケージインストール
pip install -r requirements.txt
```

### 環境変数の設定

`expense_agent/.env` を作成：
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=ここにAPIキー
GEMINI_MODEL=gemini-3-flash-preview
```

### 実行

チャットUI：
```bash
adk web
```
http://localhost:8000

APIサーバー（Swagger UI付き）：
```bash
adk api_server
```
http://localhost:8000/docs