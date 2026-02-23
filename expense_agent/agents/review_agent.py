# expense_agent/expense_agent/agents/review_agent.py

from google.adk.agents import Agent

from ..config import settings
from ..tools.review_tools import validate_journal_entry

review_agent = Agent(
    model=settings.gemini_model,
    name="review_agent",
    description="作成された仕訳の妥当性をチェックし、問題があれば指摘するエージェント",
    instruction="",
    tools=[validate_journal_entry],
)