# Expense Agent - AI仕訳自動化エージェント

Google ADK × Gemini を活用した経費精算の仕訳自動化エージェント。
レシート画像やテキスト入力から勘定科目・税区分を自動判定し、仕訳データを作成します。

## アーキテクチャ

```
ユーザー入力(テキスト / レシート画像)
        │
  root_agent(司令塔)
  ├── global_instruction ← 勘定科目ルール + 税区分ルール（全サブエージェントに届く）
  ├── instruction        ← ルート固有のワークフロー + 出力フォーマット
  ├── before_agent_callback ← state["today"] を動的注入
  │
  ├── ocr_agent       …… レシート画像 → 構造化データ  (output_key: "ocr_result")
  ├── journal_agent   …… 勘定科目・税区分判定 → 仕訳登録 (output_key: "journal_result")
  └── review_agent    …… 仕訳の妥当性チェック (output_key: "review_result")
```

マルチエージェント構成により各工程の責務を分離し、ADKのネイティブ機能でエージェント間の連携を実現しています。

### シーケンス図

[docs/sequence.md](docs/sequence.md) - テキスト入力 / レシート画像 / CSVエクスポートの3フロー

### スキーマ図

[docs/schema.md](docs/schema.md) - Pydanticモデル・ツール・勘定科目/税区分の関係

## ADKネイティブ機能の活用

### global_instruction - 全エージェント共通ルール

勘定科目ルール・税区分ルールを `global_instruction` に設定することで、ルートだけでなく全サブエージェントに自動で届きます。

```python
root_agent = Agent(
    global_instruction="\n\n".join([
        load_instruction("prompts/global/base_context.yaml"),
        load_instruction("prompts/global/account_rules.yaml"),
        load_instruction("prompts/global/tax_rules.yaml"),
    ]),
    instruction="\n\n".join([
        load_instruction("prompts/root/system_instruction.yaml"),
        load_instruction("prompts/root/output_format.yaml"),
    ]),
    ...
)
```

リファクタリング前はルートの `instruction` に全ルールを詰め込んでいたため、サブエージェントにルールが届くかどうかが会話コンテキスト依存でした。`global_instruction` により全エージェントが確実にルールを参照できます。

### session.state + {var} テンプレート - 動的値の注入

`before_agent_callback` で `state["today"]` を設定し、YAMLの `{today}` をADKが自動置換します。

```python
# callbacks.py
def set_context(callback_context: CallbackContext) -> types.Content | None:
    callback_context.state["today"] = date.today().isoformat()
    return None
```

```yaml
# prompts/global/base_context.yaml
instruction: |
  - 今日の日付: {today}
  - 「昨日」「今日」などの相対日付は、上記の今日の日付を基準に解釈する
```

リファクタリング前は `prompts/__init__.py` で `format()` による手動置換を行っていましたが、ADKのstate自動置換に任せることで `load_instruction` はYAMLを読むだけのシンプルな関数になりました。

### output_key - エージェント間のデータ受け渡し

各サブエージェントに `output_key` を設定し、最終レスポンスを `session.state` に自動保存します。

```python
ocr_agent = Agent(output_key="ocr_result", ...)
journal_agent = Agent(output_key="journal_result", ...)
```

下流のエージェントはinstructionで `{ocr_result?}` のように参照できます（`?` を付けると値が存在しない場合もエラーになりません）。リファクタリング前は会話履歴に依存したデータ受け渡しでしたが、`output_key` により確実な受け渡しが可能になりました。

## 技術スタック

- **フレームワーク**: Google ADK (Agent Development Kit)
- **LLM**: Gemini (gemini-2.0-flash / gemini-3-flash-preview)
- **型安全性**: Pydantic v2 + Enum によるバリデーション
- **設定管理**: pydantic-settings (.env)
- **プロンプト管理**: YAML外部ファイル (instruction形式で統一)
- **CI**: GitHub Actions (ruff)

## 設計方針

- **スキーマ層 = データ不変条件**: 日付形式・金額範囲・勘定科目の選択肢をPydanticで強制し、LLMの表記揺れを防止
- **ツール層 = 業務ルール**: 5,000円ルール（会議費/接待交際費）や高額チェックなど、業務固有のロジックに集中
- **エラーハンドリング**: ValidationErrorをLLMに返却し、自己修正を可能にする設計
- **テスタビリティ**: 仕訳ストアをクラス化し、テスト時のリセットやセッション分離に対応
- **フレームワークファースト**: ADKのネイティブ機能（global_instruction, session.state, output_key, callbacks）を最大限活用し、自前の実装を最小化

## ディレクトリ構成

```
expense_agent/
├── agent.py                 # ルートエージェント(司令塔)
├── callbacks.py             # before_agent_callback（state注入）
├── config.py                # 設定管理
├── agents/
│   ├── ocr_agent.py         # OCRエージェント
│   ├── journal_agent.py     # 仕訳エージェント
│   └── review_agent.py      # レビューエージェント
├── schemas/
│   ├── receipt.py           # レシートスキーマ
│   ├── journal.py           # 仕訳スキーマ
│   └── review.py            # レビュー結果スキーマ
├── tools/
│   ├── ocr_tools.py         # レシート構造化ツール
│   ├── journal_tools.py     # 仕訳登録・一覧・CSVエクスポート
│   └── review_tools.py      # 仕訳バリデーション
└── prompts/
    ├── __init__.py           # YAML読み込みユーティリティ
    ├── global/               # 全エージェント共通ルール(global_instruction)
    │   ├── base_context.yaml     # 日付・基本情報（{today}テンプレート）
    │   ├── account_rules.yaml    # 勘定科目判定ルール
    │   └── tax_rules.yaml        # 税区分判定ルール
    ├── root/                 # ルートエージェント固有(instruction)
    │   ├── system_instruction.yaml
    │   └── output_format.yaml
    └── agents/               # サブエージェント固有(各instruction)
        ├── ocr_instruction.yaml
        ├── journal_instruction.yaml
        └── review_instruction.yaml

docs/
├── sequence.md          # シーケンス図
└── schema.md            # スキーマ図
```

`prompts/` のフォルダ構成はADKの設定と対応しています。 `global/` は `global_instruction` に、`root/` はルートの `instruction` に、`agents/` は各サブエージェントの `instruction` にそれぞれ読み込まれます。

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

## テスト結果

ADK Web UIで以下の6テストを実施し、全テストPASSを確認しました。

| # | 入力 | 検証ポイント | 結果 |
|---|------|-------------|------|
| 1 | 昨日タクシーで3,500円、現金で払いました | `{today}` からの日付計算（昨日→2026-02-28） | PASS |
| 2 | コンビニで会議用のお茶とサンドイッチ、860円 | 軽減税率8%の自動判定 | PASS |
| 3 | 取引先との昼食代4,500円、クレジットカード | 5,000円境界ルール（会議費と判定） | PASS |
| 4 | 出張の航空券代150万円、クレジットカード | 高額警告 + 国内/海外の税区分確認 | PASS |
| 5 | タクシー代払いました（金額・日付なし） | 不足情報の確認要求、未確認での登録拒否 | PASS |
| 6 | 登録した仕訳をCSVで出力して | 登録済み2件のみ出力（未確認分は含まない） | PASS |

テスト3,4は提案後にユーザー確認を得ていないため未登録。テスト6のCSV出力では確認済みの2件（テスト1,2）のみが正しく出力されることを確認し、「ユーザーの確認なしに登録しない」ルールが一貫して守られていることを検証しました。

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
昨日タクシーで3,500円、現金で払いました
```

### レシート画像から仕訳

チャットUIにレシート画像をアップロードすると、OCRで読み取り → 仕訳作成 → レビューまで自動で行います。

### CSVエクスポート

```
登録した仕訳をCSVで出力して
```

freee・マネーフォワード等の会計ソフトにインポート可能なCSVを出力します。