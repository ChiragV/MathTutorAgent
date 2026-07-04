from __future__ import annotations

from skills.algebra_generation.skill import run_skill


def test_algebra_skill_returns_question_payload():
    result = run_skill({"topic": "algebra", "difficulty": "easy", "question_type": "equation"})

    assert result["topic"] == "algebra"
    assert result["difficulty"] == "easy"
    assert "question_text" in result


def test_algebra_skill_uses_requested_difficulty():
    result = run_skill({"topic": "algebra", "difficulty": "medium", "question_type": "inequality"})

    assert result["difficulty"] == "medium"
    assert result["source_skill"] == "algebra-generation"


def test_algebra_skill_includes_explanation():
    result = run_skill({"topic": "algebra", "difficulty": "hard", "question_type": "equation"})

    assert "solution" in result
    assert isinstance(result.get("hints", []), list)
