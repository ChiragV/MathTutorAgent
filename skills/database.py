from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class QuestionStore:
    """SQLite-backed store for math questions."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        if db_path is None:
            db_path = Path(__file__).resolve().parents[1] / "data" / "questions.db"
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True, parents=True)
        self._init_schema()

    def _init_schema(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id TEXT UNIQUE,
                    topic TEXT,
                    difficulty TEXT,
                    question_text TEXT,
                    answer TEXT,
                    solution TEXT,
                    source_skill TEXT,
                    trace_id TEXT,
                    created_at TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_topic_difficulty
                ON questions(topic, difficulty)
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_question_text
                ON questions(question_text)
                """
            )
            conn.commit()

    def save(self, question: dict[str, Any], trace_id: str | None = None) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO questions
                    (question_id, topic, difficulty, question_text, answer, solution, source_skill, trace_id, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        question.get("question_id"),
                        question.get("topic"),
                        question.get("difficulty"),
                        question.get("question_text"),
                        question.get("answer"),
                        question.get("solution"),
                        question.get("source_skill"),
                        trace_id,
                        datetime.now(timezone.utc).isoformat(),
                    ),
                )
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def find_similar(self, question_text: str, topic: str | None = None, threshold: float = 0.9) -> list[dict[str, Any]]:
        """Find questions similar to the given text using simple substring matching."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            if topic:
                rows = conn.execute(
                    "SELECT * FROM questions WHERE topic = ? ORDER BY created_at DESC LIMIT 100",
                    (topic,),
                ).fetchall()
            else:
                rows = conn.execute("SELECT * FROM questions ORDER BY created_at DESC LIMIT 100").fetchall()
        
        results = []
        for row in rows:
            similarity = self._similarity(question_text, row["question_text"])
            if similarity >= threshold:
                results.append({**dict(row), "similarity": similarity})
        return sorted(results, key=lambda x: x["similarity"], reverse=True)

    def find_all(self, topic: str | None = None, difficulty: str | None = None, limit: int = 10) -> list[dict[str, Any]]:
        """Retrieve stored questions."""
        query = "SELECT * FROM questions WHERE 1=1"
        params = []
        if topic:
            query += " AND topic = ?"
            params.append(topic)
        if difficulty:
            query += " AND difficulty = ?"
            params.append(difficulty)
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def count(self, topic: str | None = None) -> int:
        """Count stored questions."""
        if topic:
            with sqlite3.connect(self.db_path) as conn:
                count = conn.execute("SELECT COUNT(*) FROM questions WHERE topic = ?", (topic,)).fetchone()[0]
        else:
            with sqlite3.connect(self.db_path) as conn:
                count = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
        return count

    @staticmethod
    def _similarity(text1: str, text2: str) -> float:
        """Simple text similarity using character-level comparison."""
        if text1 == text2:
            return 1.0
        longer, shorter = (text1, text2) if len(text1) > len(text2) else (text2, text1)
        if len(longer) == 0:
            return 1.0
        matches = sum(1 for i, c in enumerate(shorter) if i < len(longer) and longer[i] == c)
        return matches / len(longer)
