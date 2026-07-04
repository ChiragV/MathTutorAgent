from __future__ import annotations

from skills.question_validator.skill import run_skill


def test_question_validator_accepts_well_formed_question():
    result = run_skill({"topic": "arithmetic", "question_text": "What is 5 + 7?"})

    assert result["is_valid"] is True
    assert result["source_skill"] == "question-validator"


def test_question_validator_flags_ambiguous_question():
    result = run_skill({"topic": "geometry", "question_text": "Find the value"})

    assert result["is_valid"] is False
    assert "reason" in result


def test_question_validator_checks_answer_presence():
    result = run_skill({"topic": "algebra", "question_text": "Solve x + 2 = 5", "answer": "3"})

    assert result["is_valid"] is True
