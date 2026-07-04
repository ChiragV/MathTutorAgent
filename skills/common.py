from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class SkillLogger:
    """Append-only JSONL logger for tracing LLM requests and skill execution."""

    def __init__(self, log_path: str | Path | None = None) -> None:
        if log_path is None:
            log_path = Path(__file__).resolve().parents[1] / "logs" / "skill_trace.jsonl"
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(exist_ok=True, parents=True)

    def log(self, event_type: str, payload: dict[str, Any]) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            **payload,
        }
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")
