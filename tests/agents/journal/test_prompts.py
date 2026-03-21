# tests/agents/journal/test_prompts.py

from expense_agent.agents.journal.prompts import JOURNAL_INSTRUCTION


def test_journal_instruction_is_string() -> None:
    assert isinstance(JOURNAL_INSTRUCTION, str)
    assert len(JOURNAL_INSTRUCTION) > 0


def test_journal_instruction_adk_template_var_intact() -> None:
    assert "{ocr_response?}" in JOURNAL_INSTRUCTION


def test_journal_instruction_tool_referenced() -> None:
    assert "create_journal_entry" in JOURNAL_INSTRUCTION