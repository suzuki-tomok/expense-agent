# expense_agent/tools/journal_tools.py

import csv
import io

from pydantic import ValidationError

from ..config import settings
from ..schemas import JournalEntry


class JournalStore:
    """仕訳データの永続化ストア"""

    def __init__(self):
        self._entries: list[JournalEntry] = []

    def add(self, entry: JournalEntry) -> JournalEntry:
        entry.id = len(self._entries) + 1
        self._entries.append(entry)
        return entry

    def list_all(self) -> list[JournalEntry]:
        return list(self._entries)

    def clear(self):
        """テスト用リセット"""
        self._entries.clear()


store = JournalStore()


def register_journal_entry(
    date: str,
    description: str,
    debit_account: str,
    credit_account: str,
    amount: int,
    tax_category: str,
    memo: str = "",
) -> dict:
    """経費の仕訳データを登録します。

    Args:
        date: 取引日(YYYY-MM-DD形式)
        description: 摘要(例: タクシー代、会議用弁当代)
        debit_account: 借方勘定科目(例: 旅費交通費、会議費)
        credit_account: 貸方勘定科目(例: 現金、未払金)
        amount: 金額(税込、円単位の整数)
        tax_category: 税区分(課税仕入10%、課税仕入8%(軽減)、非課税、不課税)
        memo: 備考(任意)

    Returns:
        dict: 登録結果
    """
    try:
        entry = JournalEntry(
            date=date,
            description=description,
            debit_account=debit_account,
            credit_account=credit_account,
            amount=amount,
            tax_category=tax_category,
            memo=memo,
        )
    except ValidationError as e:
        return {
            "status": "error",
            "message": f"バリデーションエラー: {e.errors()}",
        }

    registered = store.add(entry)
    return {
        "status": "success",
        "message": f"仕訳 #{registered.id} を登録しました",
        "entry": registered.model_dump(),
    }


def list_journal_entries() -> dict:
    """登録済みの仕訳一覧を取得します。

    Returns:
        dict: 仕訳一覧
    """
    entries = store.list_all()
    if not entries:
        return {
            "status": "success",
            "message": "登録済みの仕訳はありません",
            "entries": [],
        }
    return {
        "status": "success",
        "count": len(entries),
        "entries": [e.model_dump() for e in entries],
    }


def export_journal_csv() -> dict:
    """登録済みの仕訳データをCSV形式でエクスポートします。

    会計ソフト(freee、マネーフォワード等)へのインポートを想定したフォーマットです。

    Returns:
        dict: CSV文字列を含む結果
    """
    entries = store.list_all()
    if not entries:
        return {
            "status": "error",
            "message": "エクスポートする仕訳がありません",
        }

    headers = [
        "日付", "摘要", "借方勘定科目",
        "貸方勘定科目", "金額", "税区分", "備考",
    ]

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    for e in entries:
        writer.writerow([
            e.date,
            e.description,
            e.debit_account.value,
            e.credit_account.value,
            e.amount,
            e.tax_category.value,
            e.memo,
        ])

    csv_string = output.getvalue()

    # ファイル出力
    export_dir = settings.csv_export_dir
    export_dir.mkdir(parents=True, exist_ok=True)
    filepath = export_dir / "journal_export.csv"
    filepath.write_text(csv_string, encoding="utf-8-sig")

    return {
        "status": "success",
        "message": f"{len(entries)}件の仕訳をCSVにエクスポートしました",
        "filepath": str(filepath),
        "csv_data": csv_string,
    }