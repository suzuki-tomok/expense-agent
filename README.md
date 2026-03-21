# Expense Agent - AI仕訳自動化エージェント

Google ADK × Gemini を活用した経費精算の仕訳自動化エージェント。
レシート画像やテキスト入力から勘定科目・税区分を自動判定し、仕訳データをJSON形式で返します。

## アーキテクチャ

3つのエージェントが連携して仕訳を自動生成します。

| エージェント | 役割 |
|---|---|
| root_agent | 司令塔。入力を受け取り、サブエージェントに委譲してJSONを返す |
| ocr_agent | レシート画像を構造化データに変換する |
| journal_agent | 勘定科目・税区分を判定し仕訳データを作成する |
```
入力(テキスト or レシート画像)
    │
root_agent
    ├── ocr_agent    → OcrResponse
    └── journal_agent → JournalResponse
    │
RootResponse(JSON)
```

## 技術スタック

- **フレームワーク**: Google ADK (Agent Development Kit)
- **LLM**: Gemini (gemini-2.0-flash)
- **型安全性**: Pydantic v2 + StrEnum によるバリデーション
- **設定管理**: pydantic-settings (.env)
- **ロギング**: structlog (JSON形式 / Cloud Logging対応)
- **セッション管理**: ADK DatabaseSessionService (SQLite / PostgreSQL)
- **テスト**: pytest
- **CI**: GitHub Actions (ruff / mypy / pytest)

## 設計方針

- **APIファースト**: `output_schema=RootResponse` でJSONレスポンスを型レベルで強制
- **スキーマ層 = データ不変条件**: 日付形式・金額範囲・勘定科目をPydanticで強制し、LLMの表記揺れを防止
- **プロンプトはPythonで管理**: YAMLを廃止しPythonの文字列定数として管理。型チェック・テストの対象にする
- **エラーハンドリング**: ValidationErrorをLLMに返却し、自己修正を可能にする設計
- **マイクロサービス想定**: 認証・認可は上流APIで処理済みを前提とし、セッション管理と仕訳生成に集中

## レスポンス仕様
```python
# 成功時
{
    "status": "success",
    "data": {
        "date": "2026-03-21",
        "description": "タクシー代",
        "debit_account": "旅費交通費",
        "credit_account": "現金",
        "amount": 3500,
        "tax_category": "課税仕入10%",
        "memo": "",
        "created_at": "2026-03-21T10:00:00+00:00"
    },
    "error": null
}

# エラー時
{
    "status": "error",
    "data": null,
    "error": "バリデーションエラー: ..."
}
```

## セットアップ

### 前提条件

- Python 3.12以上
- Gemini APIキー ([Google AI Studio](https://aistudio.google.com/apikey) で取得)

### 環境構築
```bash
python -m venv .venv
source .venv/bin/activate       # Mac/Linux
# .venv\Scripts\activate        # Windows

pip install -r requirements.txt
pip install -e ".[dev]"
```

### 環境変数の設定

`expense_agent/.env` を作成:
```
GOOGLE_API_KEY=ここにAPIキー
GEMINI_MODEL=gemini-2.0-flash
GOOGLE_GENAI_USE_VERTEXAI=false
SESSION_DB_URL=sqlite+aiosqlite:///./sessions.db
```

## 実行

チャットUI:
```bash
adk web
```

APIサーバー (Swagger UI付き):
```bash
adk api_server
```

## 開発
```bash
ruff check .          # リンター
mypy expense_agent    # 型チェック
pytest tests/ -v      # テスト
```

GitHub Actions で push / PR 時に自動実行されます。