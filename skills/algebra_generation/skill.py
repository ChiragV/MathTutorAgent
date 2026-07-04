from __future__ import annotations

from typing import Any

from skills.llm.client import LLMClient


def run_skill(request: dict[str, Any], logger=None, trace_id: str | None = None) -> dict[str, Any]:
    topic = request.get("topic", "algebra")
    difficulty = request.get("difficulty", "easy")
    question_type = request.get("question_type", "equation")
    hints_requested = bool(request.get("hints_requested", False))

    prompt = (
        f"Generate one algebra question for a student. Topic: {topic}. Difficulty: {difficulty}. "
        f"Question type: {question_type}. Return concise JSON with keys question, answer, explanation, hints."
    )
    client = LLMClient()
    raw = client.generate_question(prompt, logger=logger, trace_id=trace_id)

    question_text = raw.get("question") or raw.get("question_text") or "Solve an algebra problem"
    answer = raw.get("answer") or ""
    solution = raw.get("explanation") or raw.get("solution") or "Use algebraic steps to solve the problem."
    hints = raw.get("hints") or (["Start by isolating the variable."] if hints_requested else [])

    return {
        "question_id": f"algebra-{trace_id or 'local'}",
        "question_text": question_text,
        "difficulty": difficulty,
        "answer": answer,
        "solution": solution,
        "topic": topic,
        "question_type": question_type,
        "source_skill": "algebra-generation",
        "hints": hints,
        "metadata": {"question_type": question_type, "generated_by": "llm"},
    }
