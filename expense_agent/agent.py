# expense_agent/agent.py

from google.adk.agents import Agent
from google.adk.sessions import DatabaseSessionService

from .sub_agents.journal_agent import journal_agent
from .sub_agents.ocr_agent import ocr_agent
from .sub_agents.review_agent import review_agent
from .callbacks import set_context
from .config import settings
from .db import init_db
from .prompts import load_instruction

init_db()

session_service = DatabaseSessionService(db_url=settings.session_db_url)

root_agent = Agent(
    model=settings.gemini_model,
    name="expense_root_agent",
    description="経費精算の仕訳を自動作成するAIエージェントシステム",
    global_instruction="\n\n".join([
        load_instruction("prompts/global/base_context.yaml"),
        load_instruction("prompts/global/account_rules.yaml"),
        load_instruction("prompts/global/tax_rules.yaml"),
    ]),
    instruction="\n\n".join([
        load_instruction("prompts/root/system_instruction.yaml"),
        load_instruction("prompts/root/output_format.yaml"),
    ]),
    before_agent_callback=set_context,
    sub_agents=[ocr_agent, journal_agent, review_agent],
)