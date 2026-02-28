# expense_agent/schemas/review.py

from typing import Literal

from pydantic import BaseModel, Field


class ReviewResult(BaseModel):
    """仕訳チェック結果"""

    status: Literal["ok", "warning"] = Field(description="チェック結果ステータス")
    message: str = Field(description="結果メッセージ")
    warnings: list[str] = Field(default_factory=list, description="警告リスト")
    reviewed_entry_id: int | None = Field(
        default=None,
        description="チェック対象の仕訳ID(紐付け用)",
    )
