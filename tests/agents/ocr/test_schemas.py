# tests/agents/ocr/test_schemas.py

from typing import Any

import pytest
from pydantic import ValidationError

from expense_agent.agents.ocr.schemas import OcrResponse, ReceiptItem
from expense_agent.enums import PaymentMethod, TaxRate


def _make_item(**kwargs) -> ReceiptItem:  # type: ignore[no-untyped-def]
    defaults: dict[str, Any] = {
        "name": "コーヒー",
        "price": 500,
        "tax_rate": TaxRate.STANDARD_10,
    }
    return ReceiptItem(**{**defaults, **kwargs})


def _make_ocr_response(**kwargs) -> OcrResponse:  # type: ignore[no-untyped-def]
    defaults: dict[str, Any] = {
        "store_name": "テスト店",
        "date": "2026-01-01",
        "items": [_make_item()],
        "total_amount": 500,
        "payment_method": PaymentMethod.CASH,
    }
    return OcrResponse(**{**defaults, **kwargs})


def test_ocr_response_valid() -> None:
    ocr_response = _make_ocr_response()
    assert ocr_response.store_name == "テスト店"
    assert ocr_response.total_amount == 500
    assert ocr_response.payment_method == PaymentMethod.CASH


def test_ocr_response_default_payment_method() -> None:
    ocr_response = _make_ocr_response(payment_method=PaymentMethod.UNKNOWN)
    assert ocr_response.payment_method == PaymentMethod.UNKNOWN


def test_ocr_response_invalid_date_format() -> None:
    with pytest.raises(ValidationError):
        _make_ocr_response(date="2026/01/01")


def test_ocr_response_empty_items() -> None:
    with pytest.raises(ValidationError):
        _make_ocr_response(items=[])


def test_ocr_response_zero_total() -> None:
    with pytest.raises(ValidationError):
        _make_ocr_response(total_amount=0)


def test_receipt_item_negative_price() -> None:
    with pytest.raises(ValidationError):
        _make_item(price=-1)