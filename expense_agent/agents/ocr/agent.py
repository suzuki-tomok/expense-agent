# expense_agent/agents/ocr/agent.py

from typing import Any

from google.adk.agents import Agent
from pydantic import ValidationError

from ...config import settings
from ...logger import get_logger
from .prompts import OCR_INSTRUCTION
from .schemas import OcrResponse, ReceiptItem

log = get_logger(__name__)


def parse_receipt_result(
    store_name: str,
    date: str,
    items: list[dict[str, Any]],
    total_amount: int,
    payment_method: str = "不明",
) -> dict[str, Any]:
    """レシート画像から読み取った情報を構造化して返します。

    Args:
        store_name: 店名
        date: 日付(YYYY-MM-DD形式)
        items: 品目リスト(例: [{"name": "おにぎり", "price": 160, "tax_rate": "8%"}])
        total_amount: 合計金額
        payment_method: 支払方法(現金、クレジットカード等)

    Returns:
        dict: 構造化されたレシート情報
    """
    log.info("parse_receipt_result.start", store_name=store_name, date=date)

    try:
        ocr_response = OcrResponse(
            store_name=store_name,
            date=date,
            items=[ReceiptItem(**item) for item in items],
            total_amount=total_amount,
            payment_method=payment_method,
        )
    except ValidationError as e:
        log.warning("parse_receipt_result.validation_error", errors=e.errors())
        return {"status": "error", "message": f"バリデーションエラー: {e.errors()}"}

    log.info("parse_receipt_result.success", total_amount=total_amount)
    return {"status": "success", "ocr_response": ocr_response.model_dump()}


ocr_agent = Agent(
    model=settings.gemini_model,
    name="ocr_agent",
    description="レシート画像を読み取り、構造化データに変換するエージェント",
    instruction=OCR_INSTRUCTION,
    tools=[parse_receipt_result],
    output_key="ocr_response",
)