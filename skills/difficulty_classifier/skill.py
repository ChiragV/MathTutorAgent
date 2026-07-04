from __future__ import annotations

from typing import Any

from skills.llm.client import LLMClient


def run_skill(request: dict[str, Any], logger=None, trace_id: str | None = None) -> dict[str, Any]:
    topic = request.get("topic", "arithmetic")
    difficulty = request.get("difficulty", "easy")
    question_text = request.get("question_text", "Solve a math problem")

    prompt = (
        f"Classify the difficulty of the following question for topic {topic}. "
        f"Question: {question_text}. Return JSON with keys difficulty, confidence, reason."
    )
    client = LLMClient()
    raw = client.generate_question(prompt, logger=logger, trace_id=trace_id)

    return {
        "topic": topic,
        "difficulty": raw.get("difficulty") or difficulty,
        "confidence": 0.8,
        "reason": raw.get("explanation") or raw.get("reason") or "The question appears to match the requested difficulty.",
        "source_skill": "difficulty-classifier",
    }
