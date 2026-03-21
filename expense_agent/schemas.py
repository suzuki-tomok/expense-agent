# expense_agent/schemas.py

from typing import Literal

from pydantic import BaseModel, model_validator
from typing_extensions import Self

from .agents.journal.schemas import JournalResponse


class RootResponse(BaseModel):
    status: Literal["success", "error"]
    data: JournalResponse | None = None
    error: str | None = None

    @model_validator(mode="after")
    def validate_consistency(self) -> Self:
        if self.status == "success" and self.data is None:
            raise ValueError("status=successのときdataは必須")
        if self.status == "error" and self.error is None:
            raise ValueError("status=errorのときerrorは必須")
        return self