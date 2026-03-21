# tests/agents/journal/test_tools.py

from typing import Any

from expense_agent.agents.journal.agent import create_journal_entry


def _valid_args() -> dict[str, Any]:
    return {
        "date": "2026-01-01",
        "description": "タクシー代",
        "debit_account": "旅費交通費",
        "credit_account": "現金",
        "amount": 1000,
        "tax_category": "課税仕入10%",
    }


def test_create_journal_entry_success() -> None:
    result = create_journal_entry(**_valid_args())
    assert result["status"] == "success"
    assert "journal_response" in result
    assert result["journal_response"]["amount"] == 1000
    assert result["journal_response"]["debit_account"] == "旅費交通費"


def test_create_journal_entry_future_date() -> None:
    result = create_journal_entry(**{**_valid_args(), "date": "2099-12-31"})
    assert result["status"] == "error"
    assert "message" in result


def test_create_journal_entry_invalid_account() -> None:
    args = {**_valid_args(), "debit_account": "存在しない科目"}
    result = create_journal_entry(**args)
    assert result["status"] == "error"


def test_create_journal_entry_with_memo() -> None:
    result = create_journal_entry(**{**_valid_args(), "memo": "領収書あり"})
    assert result["status"] == "success"
    assert result["journal_response"]["memo"] == "領収書あり"