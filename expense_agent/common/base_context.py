# expense_agent/common/base_context.py

from datetime import date

_TODAY = date.today().isoformat()

BASE_CONTEXT = f"""# 基本情報
- 今日の日付: {_TODAY}
- 「昨日」「今日」などの相対日付は、上記の今日の日付を基準に解釈する
- 日付は必ずYYYY-MM-DD形式で扱う"""