from __future__ import annotations

from typing import Any

from skills.llm.client import LLMClient


def run_skill(request: dict[str, Any], logger=None, trace_id: str | None = None) -> dict[str, Any]:
    topic = request.get("topic", "geometry")
    difficulty = request.get("difficulty", "easy")
    question_type = request.get("question_type", "area")
    hints_requested = bool(request.get("hints_requested", False))
    user_prompt = request.get("prompt", "")

    prompt = (
        f"Generate one geometry question for a student. Topic: {topic}. Difficulty: {difficulty}. "
        f"Question type: {question_type}. User request: {user_prompt}. "
        "Return concise JSON with keys question, answer, explanation, hints."
    )
    client = LLMClient()
    raw = client.generate_question(prompt, logger=logger, trace_id=trace_id)

    question_text = raw.get("question") or raw.get("question_text") or "Find the geometry measure"
    answer = raw.get("answer") or ""
    solution = raw.get("explanation") or raw.get("solution") or "Use the geometry rule for the shape."
    hints = raw.get("hints") or (["Label the known values first."] if hints_requested else [])

    return {
        "question_id": f"geometry-{trace_id or 'local'}",
        "question_text": question_text,
        "difficulty": difficulty,
        "answer": answer,
        "solution": solution,
        "topic": topic,
        "question_type": question_type,
        "source_skill": "geometry-generation",
        "hints": hints,
        "metadata": {"question_type": question_type, "generated_by": "llm"},
    }
