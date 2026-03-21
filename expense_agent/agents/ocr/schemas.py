# expense_agent/agents/ocr/schemas.py

from datetime import date

from pydantic import BaseModel, Field, field_validator

from ...enums import PaymentMethod, TaxRate


class ReceiptItem(BaseModel):
    name: str = Field(description="品名")
    price: int = Field(ge=0, description="金額(税込、0以上)")
    tax_rate: TaxRate = Field(description="税率(10% or 8%)")


class OcrResponse(BaseModel):
    store_name: str = Field(min_length=1, description="店名")
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$", description="日付(YYYY-MM-DD)")
    items: list[ReceiptItem] = Field(min_length=1, description="品目リスト(1件以上)")
    total_amount: int = Field(gt=0, description="合計金額(1円以上)")
    payment_method: PaymentMethod = Field(
        default=PaymentMethod.UNKNOWN,
        description="支払方法",
    )

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            date.fromisoformat(v)
        except ValueError as err:
            raise ValueError(f"無効な日付です: {v}") from err
        return v