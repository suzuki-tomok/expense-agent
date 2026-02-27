from pathlib import Path

import yaml
from google.adk.agents import Agent

from .agents.ocr_agent import ocr_agent
from .agents.journal_agent import journal_agent
from .agents.review_agent import review_agent
from .config import settings

PROMPTS_DIR = Path(__file__).parent / "prompts"


def _load_yaml(filepath: Path) -> dict:
    """YAMLファイルを読み込みdictで返す"""
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# 司令塔（ルートエージェント）向けのyamlを読み込む
root_system = _load_yaml(PROMPTS_DIR / "root" / "system_instruction.yaml")

# 業務ルール向けのyamlを読み込む
account_rules = _load_yaml(PROMPTS_DIR / "rules" / "account_rules.yaml")
tax_rules = _load_yaml(PROMPTS_DIR / "rules" / "tax_rules.yaml")
output_format = _load_yaml(PROMPTS_DIR / "rules" / "output_format.yaml")

# サブエージェント向けのyamlを読み込む
ocr_instruction = _load_yaml(PROMPTS_DIR / "agents" / "ocr_instruction.yaml")
journal_instruction = _load_yaml(PROMPTS_DIR / "agents" / "journal_instruction.yaml")
review_instruction = _load_yaml(PROMPTS_DIR / "agents" / "review_instruction.yaml")

# 各エージェントにinstructionを設定
ocr_agent.instruction = ocr_instruction["instruction"]
journal_agent.instruction = journal_instruction["instruction"]
review_agent.instruction = review_instruction["instruction"]

# ルートエージェント（司令塔）
root_agent = Agent(
    model=settings.gemini_model,
    name="expense_root_agent",
    description="経費精算の仕訳を自動作成するAIエージェントシステム",
    instruction="\n\n".join([
        root_system["instruction"],
        account_rules["instruction"],
        tax_rules["instruction"],
        output_format["instruction"],
    ]),
    sub_agents=[ocr_agent, journal_agent, review_agent],
)