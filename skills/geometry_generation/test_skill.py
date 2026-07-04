from __future__ import annotations

from skills.geometry_generation.skill import run_skill


def test_geometry_skill_returns_question_payload():
    result = run_skill({"topic": "geometry", "difficulty": "easy", "question_type": "area"})

    assert result["topic"] == "geometry"
    assert result["difficulty"] == "easy"
    assert "question_text" in result


def test_geometry_skill_supports_hard_questions():
    result = run_skill({"topic": "geometry", "difficulty": "hard", "question_type": "volume"})

    assert result["difficulty"] == "hard"
    assert result["source_skill"] == "geometry-generation"


def test_geometry_skill_includes_solution():
    result = run_skill({"topic": "geometry", "difficulty": "medium", "question_type": "perimeter"})

    assert "solution" in result
    assert isinstance(result.get("hints", []), list)
