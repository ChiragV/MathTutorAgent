from __future__ import annotations

from typing import Any

from skills.llm.client import LLMClient


def run_skill(request: dict[str, Any], logger=None, trace_id: str | None = None) -> dict[str, Any]:
    topic = request.get("topic", "fractions")
    difficulty = request.get("difficulty", "easy")
    question_type = request.get("question_type", "simplification")
    hints_requested = bool(request.get("hints_requested", False))
    user_prompt = request.get("prompt", "")

    prompt = (
        f"Generate one fraction question for a student. Topic: {topic}. Difficulty: {difficulty}. "
        f"Question type: {question_type}. User request: {user_prompt}. "
        "Return concise JSON with keys question, answer, explanation, hints."
    )
    client = LLMClient()
    raw = client.generate_question(prompt, logger=logger, trace_id=trace_id)

    question_text = raw.get("question") or raw.get("question_text") or "Simplify a fraction"
    answer = raw.get("answer") or ""
    solution = raw.get("explanation") or raw.get("solution") or "Work through the fraction carefully."
    hints = raw.get("hints") or (["Reduce the fraction if needed."] if hints_requested else [])

    return {
        "question_id": f"fraction-{trace_id or 'local'}",
        "question_text": question_text,
        "difficulty": difficulty,
        "answer": answer,
        "solution": solution,
        "topic": topic,
        "question_type": question_type,
        "source_skill": "fraction-generation",
        "hints": hints,
        "metadata": {"question_type": question_type, "generated_by": "llm"},
    }
