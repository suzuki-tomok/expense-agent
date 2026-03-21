# expense_agent/agent.py

from google.adk.agents import Agent
from google.adk.sessions import DatabaseSessionService

from .agents.journal.agent import journal_agent
from .agents.ocr.agent import ocr_agent
from .common.account_rules import ACCOUNT_RULES
from .common.base_context import BASE_CONTEXT
from .common.tax_rules import TAX_RULES
from .config import settings
from .prompts import ROOT_INSTRUCTION
from .schemas import RootResponse

session_service = DatabaseSessionService(db_url=settings.session_db_url)

root_agent = Agent(
    model=settings.gemini_model,
    name="expense_root_agent",
    description="経費精算の仕訳を自動作成するAIエージェントシステム",
    global_instruction="\n\n".join([BASE_CONTEXT, ACCOUNT_RULES, TAX_RULES]),
    instruction=ROOT_INSTRUCTION,
    output_schema=RootResponse,
    sub_agents=[ocr_agent, journal_agent],
)