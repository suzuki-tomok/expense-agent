# expense_agent/callbacks.py

from datetime import date

from google.adk.agents.callback_context import CallbackContext
from google.genai import types


def set_context(callback_context: CallbackContext) -> types.Content | None:
    """エージェント実行前にsession.stateへ動的コンテキストを注入する。"""
    callback_context.state["today"] = date.today().isoformat()
    return None
