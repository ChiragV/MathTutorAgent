from __future__ import annotations

from typing import Any

from skills.llm.client import LLMClient


def run_skill(request: dict[str, Any], logger=None, trace_id: str | None = None) -> dict[str, Any]:
    topic = request.get("topic", "arithmetic")
    question_text = request.get("question_text", "Solve a math problem")
    answer = request.get("answer")

    prompt = (
        f"Validate the following math question for topic {topic}. "
        f"Question: {question_text}. Answer provided: {answer or 'none'}. "
        "Return JSON with keys is_valid, reason, answer_present."
    )
    client = LLMClient()
    raw = client.generate_question(prompt, logger=logger, trace_id=trace_id)

    is_valid = raw.get("is_valid") if raw.get("is_valid") is not None else bool(answer or "?" in question_text)
    reason = raw.get("reason") or ("Question is solvable and clear." if is_valid else "The question is ambiguous or incomplete.")

    return {
        "topic": topic,
        "is_valid": is_valid,
        "reason": reason,
        "answer_present": bool(answer),
        "source_skill": "question-validator",
    }
