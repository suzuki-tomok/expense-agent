# expense_agent/expense_agent/agent.py

from pathlib import Path

import yaml
from google.adk.agents import Agent

from .agents.ocr_agent import ocr_agent
from .agents.journal_agent import journal_agent
from .agents.review_agent import review_agent
from .config import settings

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_yaml(filepath: Path) -> dict:
    """YAMLファイルを読み込む"""
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_root_instruction() -> str:
    """司令塔用のinstructionを組み立てる"""
    system = load_yaml(PROMPTS_DIR / "root" / "system_instruction.yaml")
    accounts = load_yaml(PROMPTS_DIR / "rules" / "account_rules.yaml")
    tax = load_yaml(PROMPTS_DIR / "rules" / "tax_rules.yaml")
    output = load_yaml(PROMPTS_DIR / "rules" / "output_format.yaml")

    instruction = f"""# 役割
{system['role']}

# ワークフロー
"""
    for step in system["workflow"]:
        instruction += f"- {step}\n"

    instruction += f"""
# 貸方勘定科目の判定
"""
    for method, account in system["credit_account_rules"].items():
        instruction += f"- {method} → {account}\n"

    instruction += "\n# 注意事項\n"
    for caution in system["cautions"]:
        instruction += f"- {caution}\n"

    instruction += "\n# 勘定科目の判定ルール\n"
    for name, rule in accounts["accounts"].items():
        instruction += f"\n## {name}\n"
        instruction += f"{rule['description']}\n"
        instruction += "対象例：\n"
        for ex in rule["examples"]:
            instruction += f"- {ex}\n"
        if "conditions" in rule:
            instruction += "判定条件：\n"
            for cond in rule["conditions"]:
                instruction += f"- {cond}\n"
        if "notes" in rule:
            instruction += f"補足：{rule['notes']}\n"
        instruction += f"デフォルト税区分：{rule['default_tax']}\n"

    if "judgement_priority" in accounts:
        instruction += "\n## 判定の優先ルール\n"
        for jp in accounts["judgement_priority"]:
            instruction += f"- {jp}\n"

    instruction += "\n# 税区分の判定ルール\n"
    for name, rule in tax["tax_categories"].items():
        instruction += f"\n## {name}\n"
        instruction += f"{rule['description']}\n"
        instruction += "対象：\n"
        for item in rule["applies_to"]:
            instruction += f"- {item}\n"
        if "notes" in rule:
            instruction += f"補足：{rule['notes']}\n"

    if "judgement_notes" in tax:
        instruction += "\n## 税区分の補足\n"
        for note in tax["judgement_notes"]:
            instruction += f"- {note}\n"

    instruction += f"""
# 出力フォーマット
{output['receipt_preview']}
{output['journal_entry_format']}
{output['confirmation_prompt']}
"""
    return instruction


def build_agent_instruction(filename: str) -> str:
    """各エージェント固有のinstructionを読み込む"""
    data = load_yaml(PROMPTS_DIR / "agents" / filename)
    return data.get("instruction", "")


# 各エージェントにinstructionを設定
ocr_agent.instruction = build_agent_instruction("ocr_instruction.yaml")
journal_agent.instruction = build_agent_instruction("journal_instruction.yaml")
review_agent.instruction = build_agent_instruction("review_instruction.yaml")

# ルートエージェント（司令塔）
root_agent = Agent(
    model=settings.gemini_model,
    name="expense_root_agent",
    description="経費精算の仕訳を自動作成するAIエージェントシステム",
    instruction=build_root_instruction(),
    sub_agents=[ocr_agent, journal_agent, review_agent],
)