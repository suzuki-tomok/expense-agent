# expense_agent/expense_agent/schemas/receipt.py

from pydantic import BaseModel, Field


class ReceiptItem(BaseModel):
    """レシートの1品目"""
    name: str = Field(description="品名")
    price: int = Field(description="金額")
    tax_rate: str = Field(description="税率（8% or 10%）")


class Receipt(BaseModel):
    """OCR読み取り結果"""
    store_name: str = Field(description="店名")
    date: str = Field(description="日付（YYYY-MM-DD）")
    items: list[ReceiptItem] = Field(description="品目リスト")
    total_amount: int = Field(description="合計金額")
    payment_method: str = Field(default="不明", description="支払方法")