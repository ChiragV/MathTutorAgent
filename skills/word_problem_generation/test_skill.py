from __future__ import annotations

from skills.word_problem_generation.skill import run_skill


def test_word_problem_skill_returns_question_payload():
    result = run_skill({"topic": "word-problems", "difficulty": "easy", "question_type": "daily-life"})

    assert result["topic"] == "word-problems"
    assert result["difficulty"] == "easy"
    assert "question_text" in result


def test_word_problem_skill_adds_context_metadata():
    result = run_skill({"topic": "word-problems", "difficulty": "medium", "question_type": "shopping"})

    assert result["source_skill"] == "word-problem-generation"
    assert result["metadata"]["context"] == "shopping"


def test_word_problem_skill_sets_solution():
    result = run_skill({"topic": "word-problems", "difficulty": "hard", "question_type": "comparison"})

    assert "solution" in result
    assert isinstance(result.get("hints", []), list)
