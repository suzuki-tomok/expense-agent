# expense_agent/expense_agent/agents/ocr_agent.py

from google.adk.agents import Agent

from ..config import settings
from ..tools.ocr_tools import parse_receipt_result

ocr_agent = Agent(
    model=settings.gemini_model,
    name="ocr_agent",
    description="レシート画像を読み取り、構造化データに変換するエージェント",
    instruction="",
    tools=[parse_receipt_result],
)