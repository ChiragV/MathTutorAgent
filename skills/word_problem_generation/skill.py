from __future__ import annotations

from typing import Any

from skills.llm.client import LLMClient


def run_skill(request: dict[str, Any], logger=None, trace_id: str | None = None) -> dict[str, Any]:
    topic = request.get("topic", "word-problems")
    difficulty = request.get("difficulty", "easy")
    question_type = request.get("question_type", "daily-life")
    hints_requested = bool(request.get("hints_requested", False))

    prompt = (
        f"Generate one word problem for a student. Topic: {topic}. Difficulty: {difficulty}. "
        f"Question type: {question_type}. Return concise JSON with keys question, answer, explanation, hints."
    )
    client = LLMClient()
    raw = client.generate_question(prompt, logger=logger, trace_id=trace_id)

    question_text = raw.get("question") or raw.get("question_text") or "Solve the word problem"
    answer = raw.get("answer") or ""
    solution = raw.get("explanation") or raw.get("solution") or "Translate the story into a math equation."
    hints = raw.get("hints") or (["Identify the quantities before solving."] if hints_requested else [])

    return {
        "question_id": f"word-problem-{trace_id or 'local'}",
        "question_text": question_text,
        "difficulty": difficulty,
        "answer": answer,
        "solution": solution,
        "topic": topic,
        "question_type": question_type,
        "source_skill": "word-problem-generation",
        "hints": hints,
        "metadata": {"context": question_type, "generated_by": "llm"},
    }
