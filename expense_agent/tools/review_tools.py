# expense_agent/expense_agent/tools/review_tools.py

from ..schemas import ReviewResult


def validate_journal_entry(
    debit_account: str,
    credit_account: str,
    amount: int,
    tax_category: str,
    description: str,
) -> dict:
    """仕訳の妥当性をチェックします。

    Args:
        debit_account: 借方勘定科目
        credit_account: 貸方勘定科目
        amount: 金額
        tax_category: 税区分
        description: 摘要

    Returns:
        dict: チェック結果
    """
    warnings: list[str] = []

    if amount <= 0:
        warnings.append("金額が0以下です")
    if amount >= 1_000_000:
        warnings.append(f"金額が{amount:,}円と高額です。確認してください")

    if debit_account == credit_account:
        warnings.append("借方と貸方が同じ勘定科目です")

    if debit_account == "接待交際費" and amount < 5000:
        warnings.append("5,000円以下の飲食は会議費の可能性があります")

    if debit_account == "会議費" and amount > 5000:
        warnings.append("5,000円超の飲食は接待交際費の可能性があります")

    if warnings:
        result = ReviewResult(
            status="warning",
            message="以下の点を確認してください",
            warnings=warnings,
        )
    else:
        result = ReviewResult(
            status="ok",
            message="チェックOK。問題ありません",
        )

    return result.model_dump()