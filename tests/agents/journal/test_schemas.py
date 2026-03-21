# tests/agents/journal/test_schemas.py

from typing import Any

import pytest
from pydantic import ValidationError

from expense_agent.agents.journal.schemas import JournalResponse
from expense_agent.enums import CreditAccount, DebitAccount, TaxCategory


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


def test_journal_response_valid() -> None:
    journal_response = _make_journal_response()
    assert journal_response.description == "タクシー代"
    assert journal_response.amount == 1000


def test_journal_response_future_date() -> None:
    with pytest.raises(ValidationError):
        _make_journal_response(date="2099-12-31")


def test_journal_response_invalid_date_format() -> None:
    with pytest.raises(ValidationError):
        _make_journal_response(date="2026/01/01")


def test_journal_response_zero_amount() -> None:
    with pytest.raises(ValidationError):
        _make_journal_response(amount=0)


def test_journal_response_memo_default_empty() -> None:
    journal_response = _make_journal_response()
    assert journal_response.memo == ""


def test_journal_response_created_at_timezone_aware() -> None:
    from datetime import timezone
    journal_response = _make_journal_response()
    assert journal_response.created_at.tzinfo == timezone.utc