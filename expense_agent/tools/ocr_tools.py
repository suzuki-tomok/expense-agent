# expense_agent/expense_agent/tools/ocr_tools.py

from ..schemas import Receipt, ReceiptItem


def parse_receipt_result(
    store_name: str,
    date: str,
    items: list[dict],
    total_amount: int,
    payment_method: str = "不明",
) -> dict:
    """レシート画像から読み取った情報を構造化して返します。

    Args:
        store_name: 店名
        date: 日付（YYYY-MM-DD形式）
        items: 品目リスト（例：[{"name": "おにぎり", "price": 160, "tax_rate": "8%"}]）
        total_amount: 合計金額
        payment_method: 支払方法（現金、クレジットカード等）

    Returns:
        dict: 構造化されたレシート情報
    """
    receipt = Receipt(
        store_name=store_name,
        date=date,
        items=[ReceiptItem(**item) for item in items],
        total_amount=total_amount,
        payment_method=payment_method,
    )
    return {
        "status": "success",
        "receipt": receipt.model_dump(),
    }