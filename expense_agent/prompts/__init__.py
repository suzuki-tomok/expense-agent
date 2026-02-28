# expense_agent/prompts/__init__.py

from pathlib import Path

import yaml

PACKAGE_DIR = Path(__file__).parent.parent


def load_instruction(filepath: str) -> str:
    """YAMLファイルからinstruction文字列を読み込む。

    Args:
        filepath: expense_agentパッケージルートからの相対パス
                  例: "prompts/agents/ocr_instruction.yaml"

    Returns:
        instruction文字列
    """
    path = PACKAGE_DIR / filepath
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data["instruction"]