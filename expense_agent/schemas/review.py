# expense_agent/expense_agent/schemas/review.py

from pydantic import BaseModel, Field


class ReviewResult(BaseModel):
    """チェック結果"""
    status: str = Field(description="ok or warning")
    message: str
    warnings: list[str] = Field(default_factory=list)