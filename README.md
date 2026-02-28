# Expense Agent - AI仕訳自動化エージェント

Google ADK × Gemini を活用した経費精算の仕訳自動化エージェント。
レシート画像やテキスト入力から勘定科目・税区分を自動判定し、仕訳データを作成します。

## アーキテクチャ

```
ユーザー入力(テキスト / レシート画像)
        │
  root_agent(司令塔)
        ├── ocr_agent …… レシート画像 → 構造化データ
        ├── journal_agent …… 勘定科目・税区分判定 → 仕訳登録
        └── review_agent …… 仕訳の妥当性チェック
```

マルチエージェント構成により、各工程の責務を分離しています。

## 技術スタック

- **フレームワーク**: Google ADK (Agent Development Kit)
- **LLM**: Gemini (gemini-2.0-flash / gemini-3-flash-preview)
- **型安全性**: Pydantic v2 + Enum によるバリデーション
- **設定管理**: pydantic-settings (.env)
- **プロンプト管理**: YAML外部ファイル (instruction形式で統一)
- **CI**: GitHub Actions (ruff)

## 設計方針

- **スキーマ層 = データ不変条件**: 日付形式・金額範囲・勘定科目の選択肢をPydanticで強制し、LLMの表記揺れを防止
- **ツール層 = 業務ルール**: 5,000円ルール(会議費/接待交際費)や高額チェックなど、業務固有のロジックに集中
- **エラーハンドリング**: ValidationErrorをLLMに返却し、自己修正を可能にする設計
- **テスタビリティ**: 仕訳ストアをクラス化し、テスト時のリセットやセッション分離に対応

## ディレクトリ構成

```
expense_agent/
├── agent.py                 # ルートエージェント(司令塔)
├── config.py                # 設定管理
├── agents/
│   ├── ocr_agent.py         # OCRエージェント
│   ├── journal_agent.py     # 仕訳エージェント
│   └── review_agent.py      # レビューエージェント
├── schemas/
│   ├── enums.py             # Enum定義(勘定科目・税区分・支払方法)
│   ├── receipt.py           # レシートスキーマ
│   ├── journal.py           # 仕訳スキーマ
│   └── review.py            # レビュー結果スキーマ
├── tools/
│   ├── ocr_tools.py         # レシート構造化ツール
│   ├── journal_tools.py     # 仕訳登録・一覧・CSVエクスポート
│   └── review_tools.py      # 仕訳バリデーション
└── prompts/
    ├── __init__.py           # YAML読み込みユーティリティ
    ├── root/
    │   └── system_instruction.yaml
    ├── agents/
    │   ├── ocr_instruction.yaml
    │   ├── journal_instruction.yaml
    │   └── review_instruction.yaml
    └── rules/
        ├── account_rules.yaml    # 勘定科目判定ルール
        ├── tax_rules.yaml        # 税区分判定ルール
        └── output_format.yaml    # 出力フォーマット
```

## セットアップ

### 前提条件

- Python 3.12
- Gemini APIキー (https://aistudio.google.com/apikey で取得)

### 環境構築

```bash
cd expense-agent

# 仮想環境の作成と有効化
python -m venv .venv
source .venv/Scripts/activate  # Git Bash
# .venv\Scripts\activate       # PowerShell

# パッケージインストール
pip install -r requirements.txt
```

### 環境変数の設定

`expense_agent/.env` を作成:

```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=ここにAPIキー
GEMINI_MODEL=gemini-3-flash-preview
CSV_EXPORT_DIR=./exports
```

## 実行

チャットUI:

```bash
adk web
```

http://localhost:8000

APIサーバー (Swagger UI付き):

```bash
adk api_server
```

http://localhost:8000/docs

## 開発

### リンター / フォーマッター (ruff)

```bash
# チェック
ruff check .

# 自動修正
ruff check --fix .

# フォーマット
ruff format .
```

設定は `pyproject.toml` の `[tool.ruff]` セクションで管理しています。

### 型チェック (mypy)

```bash
mypy expense_agent
```

strict モードで実行されます。Pydantic v2 のプラグインを有効化済みです。

### CI

GitHub Actions で push / PR 時に ruff と mypy を自動実行します。

## 使い方

### テキスト入力で仕訳

```
2/28にタクシーで3,500円、現金で払いました
```

### レシート画像から仕訳

チャットUIにレシート画像をアップロードすると、OCRで読み取り → 仕訳作成 → レビューまで自動で行います。

### CSVエクスポート

```
仕訳をCSVで出力して
```

freee・マネーフォワード等の会計ソフトにインポート可能なCSVを出力します。