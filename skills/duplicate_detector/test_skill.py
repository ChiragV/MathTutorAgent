from __future__ import annotations

import uuid

from skills.duplicate_detector.skill import run_skill


def test_duplicate_detector_marks_unique_question():
    unique_text = f"Unique question {uuid.uuid4()}"
    result = run_skill({"topic": "arithmetic", "question_text": unique_text})

    assert result["topic"] == "arithmetic"
    assert result["source_skill"] == "duplicate-detector"


def test_duplicate_detector_flags_similar_question():
    result = run_skill({"topic": "arithmetic", "question_text": "What is 8 + 4?", "history": [{"question_text": "What is 8 + 4?"}]})

    assert result["is_duplicate"] is True


def test_duplicate_detector_reports_similarity_score():
    result = run_skill({"topic": "algebra", "question_text": "Solve 2x + 1 = 7", "history": [{"question_text": "Solve 2x + 1 = 7"}]})

    assert 0 <= result["similarity_score"] <= 1
