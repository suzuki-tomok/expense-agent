# expense_agent/tools/review_tools.py

from typing import Any

from ..schemas import ReviewResult
from ..schemas.enums import DebitAccount


def validate_journal_entry(
    entry_id: int,
    debit_account: str,
    credit_account: str,
    amount: int,
    tax_category: str,
    description: str,
) -> dict[str, Any]:
    """仕訳の妥当性をチェックします。

    Args:
        entry_id: チェック対象の仕訳ID
        debit_account: 借方勘定科目
        credit_account: 貸方勘定科目
        amount: 金額
        tax_category: 税区分
        description: 摘要

    Returns:
        dict: チェック結果
    """
    warnings: list[str] = []

    # 業務ルール: 高額チェック
    if amount >= 1_000_000:
        warnings.append(f"金額が{amount:,}円と高額です。確認してください")

    # 業務ルール: 借方=貸方チェック
    if debit_account == credit_account:
        warnings.append("借方と貸方が同じ勘定科目です")

    # 業務ルール: 5,000円ルール(飲食関連)
    if debit_account == DebitAccount.ENTERTAINMENT.value and amount < 5000:
        warnings.append("5,000円以下の飲食は会議費の可能性があります")

    if debit_account == DebitAccount.MEETING.value and amount > 5000:
        warnings.append("5,000円超の飲食は接待交際費の可能性があります")

    if warnings:
        result = ReviewResult(
            status="warning",
            message="以下の点を確認してください",
            warnings=warnings,
            reviewed_entry_id=entry_id,
        )
    else:
        result = ReviewResult(
            status="ok",
            message="チェックOK。問題ありません",
            reviewed_entry_id=entry_id,
        )

    return result.model_dump()
