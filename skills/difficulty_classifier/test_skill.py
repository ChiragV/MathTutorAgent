from __future__ import annotations

from skills.difficulty_classifier.skill import run_skill


def test_difficulty_classifier_returns_label_and_score():
    result = run_skill({"topic": "arithmetic", "difficulty": "easy", "question_text": "What is 2 + 3?"})

    assert result["topic"] == "arithmetic"
    assert result["difficulty"] == "easy"
    assert 0 <= result["confidence"] <= 1


def test_difficulty_classifier_handles_hard_request():
    result = run_skill({"topic": "algebra", "difficulty": "hard", "question_text": "Solve 3x + 4 = 19"})

    assert result["difficulty"] == "hard"
    assert result["source_skill"] == "difficulty-classifier"


def test_difficulty_classifier_includes_reasoning():
    result = run_skill({"topic": "geometry", "difficulty": "medium", "question_text": "Find the area of a rectangle"})

    assert "reason" in result
