# expense_agent/expense_agent/schemas/journal.py

from datetime import datetime

from pydantic import BaseModel, Field


class JournalEntry(BaseModel):
    """仕訳データ"""
    id: int
    date: str
    description: str
    debit_account: str
    credit_account: str
    amount: int
    tax_category: str
    memo: str = ""
    created_at: datetime = Field(default_factory=datetime.now)