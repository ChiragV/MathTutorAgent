#!/usr/bin/env python
"""Query the question store for analysis and debugging."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from skills.database import QuestionStore

ROOT = Path(__file__).resolve().parent


def show_stats() -> None:
    store = QuestionStore(ROOT / "data" / "questions.db")
    print("\n📊 Question Store Statistics")
    print(f"{'='*60}")
    
    total = store.count()
    print(f"Total questions: {total}")
    
    for topic in ["arithmetic", "algebra", "fractions", "geometry", "word-problems"]:
        count = store.count(topic=topic)
        if count > 0:
            print(f"  - {topic}: {count}")
    print()


def show_recent(topic: str | None = None, limit: int = 5) -> None:
    store = QuestionStore(ROOT / "data" / "questions.db")
    questions = store.find_all(topic=topic, limit=limit)
    
    if not questions:
        print(f"No questions found{f' for topic {topic}' if topic else ''}.")
        return
    
    print(f"\n📝 Recent Questions{f' ({topic})' if topic else ''}:")
    print(f"{'='*60}")
    for q in questions:
        print(f"ID: {q['question_id']}")
        print(f"Topic: {q['topic']} | Difficulty: {q['difficulty']}")
        print(f"Q: {q['question_text'][:70]}...")
        print(f"A: {q['answer']}")
        print(f"Trace: {q['trace_id']}")
        print("-" * 60)
    print()


def find_duplicates(question_text: str, topic: str | None = None) -> None:
    store = QuestionStore(ROOT / "data" / "questions.db")
    similar = store.find_similar(question_text, topic=topic, threshold=0.80)
    
    if not similar:
        print(f"✓ No similar questions found for: {question_text[:60]}...")
        return
    
    print(f"\n⚠️  Found {len(similar)} similar question(s):")
    print(f"{'='*60}")
    for item in similar:
        print(f"Similarity: {item['similarity']:.2%} | {item['question_text'][:60]}...")
        print(f"  Trace: {item['trace_id']}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the question store")
    parser.add_argument("--stats", action="store_true", help="Show store statistics")
    parser.add_argument("--recent", type=int, default=0, help="Show N recent questions")
    parser.add_argument("--topic", help="Filter by topic")
    parser.add_argument("--find-duplicates", help="Find similar questions")
    args = parser.parse_args()

    if args.stats:
        show_stats()
    elif args.recent > 0:
        show_recent(topic=args.topic, limit=args.recent)
    elif args.find_duplicates:
        find_duplicates(args.find_duplicates, topic=args.topic)
    else:
        show_stats()
        show_recent(limit=3)
