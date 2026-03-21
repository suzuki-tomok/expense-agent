# tests/agents/ocr/test_tools.py

from typing import Any

from expense_agent.agents.ocr.agent import parse_receipt_result


def _valid_items() -> list[dict[str, Any]]:
    return [{"name": "コーヒー", "price": 500, "tax_rate": "10%"}]


def test_parse_receipt_result_success() -> None:
    result = parse_receipt_result(
        store_name="テスト店",
        date="2026-01-01",
        items=_valid_items(),
        total_amount=500,
        payment_method="現金",
    )
    assert result["status"] == "success"
    assert "ocr_response" in result
    assert result["ocr_response"]["store_name"] == "テスト店"
    assert result["ocr_response"]["total_amount"] == 500


def test_parse_receipt_result_invalid_date() -> None:
    result = parse_receipt_result(
        store_name="テスト店",
        date="invalid-date",
        items=_valid_items(),
        total_amount=500,
    )
    assert result["status"] == "error"
    assert "message" in result


def test_parse_receipt_result_invalid_item() -> None:
    result = parse_receipt_result(
        store_name="テスト店",
        date="2026-01-01",
        items=[{"name": "コーヒー", "price": -1, "tax_rate": "10%"}],
        total_amount=500,
    )
    assert result["status"] == "error"