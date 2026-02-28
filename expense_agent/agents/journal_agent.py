# expense_agent/agents/journal_agent.py

from google.adk.agents import Agent

from ..config import settings
from ..prompts import load_instruction
from ..tools.journal_tools import (
    export_journal_csv,
    list_journal_entries,
    register_journal_entry,
)

journal_agent = Agent(
    model=settings.gemini_model,
    name="journal_agent",
    description="経費情報から勘定科目と税区分を判定し、仕訳データを作成するエージェント",
    instruction=load_instruction("prompts/agents/journal_instruction.yaml"),
    tools=[
        register_journal_entry,
        list_journal_entries,
        export_journal_csv,
    ],
)
