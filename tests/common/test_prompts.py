# tests/common/test_prompts.py

import re

from expense_agent.common.account_rules import ACCOUNT_RULES
from expense_agent.common.base_context import BASE_CONTEXT
from expense_agent.common.tax_rules import TAX_RULES


def test_base_context_is_string() -> None:
    assert isinstance(BASE_CONTEXT, str)
    assert len(BASE_CONTEXT) > 0


def test_base_context_today_embedded() -> None:
    assert "{_TODAY}" not in BASE_CONTEXT
    assert re.search(r"\d{4}-\d{2}-\d{2}", BASE_CONTEXT)


def test_account_rules_is_string() -> None:
    assert isinstance(ACCOUNT_RULES, str)
    assert len(ACCOUNT_RULES) > 0


def test_account_rules_contains_key_accounts() -> None:
    assert "旅費交通費" in ACCOUNT_RULES
    assert "会議費" in ACCOUNT_RULES
    assert "接待交際費" in ACCOUNT_RULES


def test_tax_rules_is_string() -> None:
    assert isinstance(TAX_RULES, str)
    assert len(TAX_RULES) > 0


def test_tax_rules_contains_key_categories() -> None:
    assert "課税仕入10%" in TAX_RULES
    assert "課税仕入8%" in TAX_RULES
    assert "非課税" in TAX_RULES
    assert "不課税" in TAX_RULES