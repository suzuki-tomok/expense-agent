# expense_agent/agents/journal/agent.py

from typing import Any

from google.adk.agents import Agent
from pydantic import ValidationError

from ...config import settings
from ...logger import get_logger
from .prompts import JOURNAL_INSTRUCTION
from .schemas import JournalResponse

log = get_logger(__name__)


def create_journal_entry(
    date: str,
    description: str,
    debit_account: str,
    credit_account: str,
    amount: int,
    tax_category: str,
    memo: str = "",
) -> dict[str, Any]:
    """経費の仕訳データを作成して返します。

    Args:
        date: 取引日(YYYY-MM-DD形式)
        description: 摘要(例: タクシー代、会議用弁当代)
        debit_account: 借方勘定科目(例: 旅費交通費、会議費)
        credit_account: 貸方勘定科目(例: 現金、未払金)
        amount: 金額(税込、円単位の整数)
        tax_category: 税区分(課税仕入10%、課税仕入8%(軽減)、非課税、不課税)
        memo: 備考(任意)

    Returns:
        dict: 作成した仕訳データ
    """
    log.info(
        "create_journal_entry.start",
        date=date,
        amount=amount,
        debit_account=debit_account,
    )

    try:
        journal_response = JournalResponse(
            date=date,
            description=description,
            debit_account=debit_account,
            credit_account=credit_account,
            amount=amount,
            tax_category=tax_category,
            memo=memo,
        )
    except ValidationError as e:
        log.warning("create_journal_entry.validation_error", errors=e.errors())
        return {"status": "error", "message": f"バリデーションエラー: {e.errors()}"}

    log.info(
        "create_journal_entry.success",
        debit_account=debit_account,
        amount=amount,
    )
    return {"status": "success", "journal_response": journal_response.model_dump()}


journal_agent = Agent(
    model=settings.gemini_model,
    name="journal_agent",
    description="経費情報から勘定科目と税区分を判定し、仕訳データを作成するエージェント",
    instruction=JOURNAL_INSTRUCTION,
    tools=[create_journal_entry],
    output_key="journal_response",
)