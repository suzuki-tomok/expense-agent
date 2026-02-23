# expense_agent/expense_agent/tools/journal_tools.py

import csv
import io
import os

from ..schemas import JournalEntry

journal_entries: list[JournalEntry] = []


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
        date: 取引日（YYYY-MM-DD形式）
        description: 摘要（例：タクシー代、会議用弁当代）
        debit_account: 借方勘定科目（例：旅費交通費、会議費）
        credit_account: 貸方勘定科目（例：現金、未払金）
        amount: 金額（税込、円単位の整数）
        tax_category: 税区分（課税仕入10%、課税仕入8%（軽減）、非課税、不課税）
        memo: 備考（任意）

    Returns:
        dict: 登録結果
    """
    entry = JournalEntry(
        id=len(journal_entries) + 1,
        date=date,
        description=description,
        debit_account=debit_account,
        credit_account=credit_account,
        amount=amount,
        tax_category=tax_category,
        memo=memo,
    )
    journal_entries.append(entry)
    return {
        "status": "success",
        "message": f"仕訳 #{entry.id} を登録しました",
        "entry": entry.model_dump(),
    }


def list_journal_entries() -> dict:
    """登録済みの仕訳一覧を取得します。

    Returns:
        dict: 仕訳一覧
    """
    if not journal_entries:
        return {
            "status": "success",
            "message": "登録済みの仕訳はありません",
            "entries": [],
        }
    return {
        "status": "success",
        "count": len(journal_entries),
        "entries": [e.model_dump() for e in journal_entries],
    }


def export_journal_csv() -> dict:
    """登録済みの仕訳データをCSV形式でエクスポートします。
    会計ソフト（freee、マネーフォワード等）へのインポートを想定したフォーマットです。

    Returns:
        dict: CSV文字列を含む結果
    """
    if not journal_entries:
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
    for e in journal_entries:
        writer.writerow([
            e.date,
            e.description,
            e.debit_account,
            e.credit_account,
            e.amount,
            e.tax_category,
            e.memo,
        ])

    csv_string = output.getvalue()

    filepath = os.path.join(
        os.path.dirname(__file__), "..", "journal_export.csv"
    )
    with open(filepath, "w", encoding="utf-8-sig") as f:
        f.write(csv_string)

    return {
        "status": "success",
        "message": f"{len(journal_entries)}件の仕訳をCSVにエクスポートしました",
        "csv_data": csv_string,
    }