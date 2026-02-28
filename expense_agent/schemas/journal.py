# expense_agent/schemas/journal.py

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from .enums import CreditAccount, DebitAccount, TaxCategory


class JournalEntry(BaseModel):
    """仕訳データ"""
    id: int = Field(default=0, exclude=True, description="サーバー側で自動採番")
    date: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="取引日(YYYY-MM-DD)",
    )
    description: str = Field(min_length=1, description="摘要")
    debit_account: DebitAccount = Field(description="借方勘定科目")
    credit_account: CreditAccount = Field(description="貸方勘定科目")
    amount: int = Field(gt=0, description="金額(税込、1円以上)")
    tax_category: TaxCategory = Field(description="税区分")
    memo: str = Field(default="", description="備考")
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        from datetime import date

        try:
            parsed = date.fromisoformat(v)
        except ValueError:
            raise ValueError(f"無効な日付です: {v}")
        if parsed > date.today():
            raise ValueError(f"未来日は登録できません: {v}")
        return v