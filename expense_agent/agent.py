# expense_agent/agent.py

from google.adk.agents import Agent

from .agents.journal_agent import journal_agent
from .agents.ocr_agent import ocr_agent
from .agents.review_agent import review_agent
from .config import settings
from .prompts import load_instruction

# ルートエージェント(司令塔)
root_agent = Agent(
    model=settings.gemini_model,
    name="expense_root_agent",
    description="経費精算の仕訳を自動作成するAIエージェントシステム",
    instruction="\n\n".join([
        load_instruction("prompts/root/system_instruction.yaml"),
        load_instruction("prompts/rules/account_rules.yaml"),
        load_instruction("prompts/rules/tax_rules.yaml"),
        load_instruction("prompts/rules/output_format.yaml"),
    ]),
    sub_agents=[ocr_agent, journal_agent, review_agent],
)