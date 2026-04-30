"""Small shared helper functions for the project."""

from pathlib import Path
from typing import Any

import json


def save_json(data: dict[str, Any], path: str | Path) -> None:
    """Save a dictionary as formatted UTF-8 JSON."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
