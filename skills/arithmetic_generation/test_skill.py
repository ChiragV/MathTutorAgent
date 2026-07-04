from __future__ import annotations

from skills.arithmetic_generation.skill import run_skill


def test_arithmetic_skill_returns_question_payload():
    result = run_skill({"topic": "arithmetic", "difficulty": "easy", "question_type": "addition"})

    assert result["topic"] == "arithmetic"
    assert result["difficulty"] == "easy"
    assert "question_text" in result
    assert "answer" in result


def test_arithmetic_skill_supports_hints():
    result = run_skill({"topic": "arithmetic", "difficulty": "medium", "question_type": "multiplication", "hints_requested": True})

    assert result["question_type"] == "multiplication"
    assert isinstance(result.get("hints", []), list)


def test_arithmetic_skill_uses_skill_metadata():
    result = run_skill({"topic": "arithmetic", "difficulty": "hard", "question_type": "division"})

    assert result["source_skill"] == "arithmetic-generation"
    assert result["metadata"]["operation"] == "division"
