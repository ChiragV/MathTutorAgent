from __future__ import annotations

from typing import Any

from skills.database import QuestionStore
from skills.llm.client import LLMClient


def run_skill(request: dict[str, Any], logger=None, trace_id: str | None = None) -> dict[str, Any]:
    topic = request.get("topic", "arithmetic")
    question_text = request.get("question_text", "Solve a math problem")
    history = request.get("history") or []

    store = QuestionStore()
    similar = store.find_similar(question_text, topic=topic, threshold=0.85)
    
    is_duplicate = len(similar) > 0
    similarity_score = similar[0]["similarity"] if similar else 0.0
    
    if not is_duplicate:
        prompt = (
            f"Compare the following question against prior questions for topic {topic}. "
            f"Question: {question_text}. History: {history}. Return JSON with keys is_duplicate, similarity_score, reason."
        )
        client = LLMClient()
        raw = client.generate_question(prompt, logger=logger, trace_id=trace_id)
        is_duplicate = bool(raw.get("is_duplicate")) or any(item.get("question_text") == question_text for item in history)
        similarity_score = raw.get("similarity_score") or 0.0

    return {
        "topic": topic,
        "is_duplicate": is_duplicate,
        "similarity_score": similarity_score,
        "reason": f"Found {len(similar)} similar question(s)" if similar else "The question appears to be unique.",
        "source_skill": "duplicate-detector",
    }
