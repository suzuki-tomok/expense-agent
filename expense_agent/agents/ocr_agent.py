# expense_agent/agents/ocr_agent.py

from google.adk.agents import Agent

from ..config import settings
from ..prompts import load_instruction
from ..tools.ocr_tools import parse_receipt_result

ocr_agent = Agent(
    model=settings.gemini_model,
    name="ocr_agent",
    description="レシート画像を読み取り、構造化データに変換するエージェント",
    instruction=load_instruction("prompts/agents/ocr_instruction.yaml"),
    tools=[parse_receipt_result],
    output_key="ocr_result",
)
