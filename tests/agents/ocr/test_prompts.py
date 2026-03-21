# tests/agents/ocr/test_prompts.py

import re

from expense_agent.agents.ocr.prompts import OCR_INSTRUCTION


def test_ocr_instruction_is_string() -> None:
    assert isinstance(OCR_INSTRUCTION, str)
    assert len(OCR_INSTRUCTION) > 0


def test_ocr_instruction_today_embedded() -> None:
    assert "{_TODAY}" not in OCR_INSTRUCTION
    assert re.search(r"\d{4}-\d{2}-\d{2}", OCR_INSTRUCTION)


def test_ocr_instruction_tool_referenced() -> None:
    assert "parse_receipt_result" in OCR_INSTRUCTION