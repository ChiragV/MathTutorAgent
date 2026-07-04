from __future__ import annotations

from skills.fraction_generation.skill import run_skill


def test_fraction_skill_returns_question_payload():
    result = run_skill({"topic": "fractions", "difficulty": "easy", "question_type": "simplification"})

    assert result["topic"] == "fractions"
    assert result["difficulty"] == "easy"
    assert "question_text" in result


def test_fraction_skill_returns_solution_and_hints():
    result = run_skill({"topic": "fractions", "difficulty": "medium", "question_type": "addition"})

    assert "solution" in result
    assert isinstance(result.get("hints", []), list)


def test_fraction_skill_sets_source_skill():
    result = run_skill({"topic": "fractions", "difficulty": "hard", "question_type": "comparison"})

    assert result["source_skill"] == "fraction-generation"
