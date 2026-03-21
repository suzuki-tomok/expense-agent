# tests/test_schemas.py

from typing import Any

import pytest
from pydantic import ValidationError

from expense_agent.agents.journal.schemas import JournalResponse
from expense_agent.enums import CreditAccount, DebitAccount, TaxCategory
from expense_agent.schemas import RootResponse


def _make_journal_response(**kwargs) -> JournalResponse:  # type: ignore[no-untyped-def]
    defaults: dict[str, Any] = {
        "date": "2026-01-01",
        "description": "タクシー代",
        "debit_account": DebitAccount.TRAVEL,
        "credit_account": CreditAccount.CASH,
        "amount": 1000,
        "tax_category": TaxCategory.TAXABLE_10,
    }
    return JournalResponse(**{**defaults, **kwargs})


def test_root_response_success() -> None:
    journal_response = _make_journal_response()
    root_response = RootResponse(status="success", data=journal_response)
    assert root_response.status == "success"
    assert root_response.data is not None
    assert root_response.data.amount == 1000
    assert root_response.error is None


def test_root_response_error() -> None:
    root_response = RootResponse(status="error", error="処理に失敗しました")
    assert root_response.status == "error"
    assert root_response.error == "処理に失敗しました"
    assert root_response.data is None


def test_root_response_success_without_data_fails() -> None:
    with pytest.raises(ValidationError):
        RootResponse(status="success", data=None)


def test_root_response_error_without_message_fails() -> None:
    with pytest.raises(ValidationError):
        RootResponse(status="error", error=None)