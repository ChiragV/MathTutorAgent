from __future__ import annotations

import argparse
import importlib
import json
import uuid
from pathlib import Path
from typing import Any

from skills.common import SkillLogger
from skills.database import QuestionStore
from skills.llm.client import LLMClient

ROOT = Path(__file__).resolve().parent
STORE = QuestionStore(ROOT / "data" / "questions.db")
SKILLS = {
    "arithmetic-generation": {
        "module": "skills.arithmetic_generation.skill",
        "description_path": ROOT / "skills" / "arithmetic_generation" / "skill.md",
    },
    "algebra-generation": {
        "module": "skills.algebra_generation.skill",
        "description_path": ROOT / "skills" / "algebra_generation" / "skill.md",
    },
    "fraction-generation": {
        "module": "skills.fraction_generation.skill",
        "description_path": ROOT / "skills" / "fraction_generation" / "skill.md",
    },
    "geometry-generation": {
        "module": "skills.geometry_generation.skill",
        "description_path": ROOT / "skills" / "geometry_generation" / "skill.md",
    },
    "word-problem-generation": {
        "module": "skills.word_problem_generation.skill",
        "description_path": ROOT / "skills" / "word_problem_generation" / "skill.md",
    },
    "difficulty-classifier": {
        "module": "skills.difficulty_classifier.skill",
        "description_path": ROOT / "skills" / "difficulty_classifier" / "skill.md",
    },
    "question-validator": {
        "module": "skills.question_validator.skill",
        "description_path": ROOT / "skills" / "question_validator" / "skill.md",
    },
    "duplicate-detector": {
        "module": "skills.duplicate_detector.skill",
        "description_path": ROOT / "skills" / "duplicate_detector" / "skill.md",
    },
}


def load_skill_descriptions() -> dict[str, str]:
    descriptions: dict[str, str] = {}
    for skill_name, metadata in SKILLS.items():
        description_path = metadata["description_path"]
        if description_path.exists():
            descriptions[skill_name] = description_path.read_text(encoding="utf-8")
        else:
            descriptions[skill_name] = skill_name
    return descriptions


def select_skill(request: dict[str, Any], logger: SkillLogger | None, trace_id: str) -> str:
    descriptions = load_skill_descriptions()
    prompt = (
        "You are the router for a math tutor. Choose exactly one skill based on the user's request. "
        "Use only the skill descriptions below; do not invent skills. Return JSON with keys 'skill' and 'reason'.\n"
        f"User request: {json.dumps(request, ensure_ascii=False)}\n"
        "Skill descriptions:\n"
    )
    for name, description in descriptions.items():
        prompt += f"- {name}: {description.splitlines()[0]}\n"

    client = LLMClient()
    raw = client.generate_text(prompt, logger=logger, trace_id=trace_id)
    logger.log("skill_selection_prompt", {"trace_id": trace_id, "prompt": prompt}) if logger else None
    logger.log("skill_selection_response", {"trace_id": trace_id, "response": raw}) if logger else None

    try:
        payload = json.loads(raw)
        skill_name = payload.get("skill")
    except Exception:
        skill_name = None

    if skill_name in SKILLS:
        return skill_name

    prompt_text = str(request.get("prompt") or request.get("topic") or "").lower()
    if any(term in prompt_text for term in ["generate", "question", "problem", "make"]):
        if any(term in prompt_text for term in ["algebra", "equation", "variable"]):
            return "algebra-generation"
        if any(term in prompt_text for term in ["fraction", "fractional"]):
            return "fraction-generation"
        if any(term in prompt_text for term in ["geometry", "area", "perimeter", "volume"]):
            return "geometry-generation"
        if any(term in prompt_text for term in ["word", "story"]):
            return "word-problem-generation"
        return "arithmetic-generation"
    if any(term in prompt_text for term in ["classify", "difficulty"]):
        return "difficulty-classifier"
    if any(term in prompt_text for term in ["validate", "valid", "ambiguous"]):
        return "question-validator"
    if any(term in prompt_text for term in ["duplicate", "similar"]):
        return "duplicate-detector"
    return "arithmetic-generation"


def process_request(request: dict[str, Any], logger: SkillLogger | None = None, trace_id: str | None = None) -> dict[str, Any]:
    trace_id = trace_id or str(uuid.uuid4())
    if logger is None:
        logger = SkillLogger(ROOT / "logs" / "trace.jsonl")

    logger.log("orchestrator_request", {"trace_id": trace_id, "request": request})
    selected_skill = select_skill(request, logger, trace_id)
    logger.log("orchestrator_selection", {"trace_id": trace_id, "selected_skill": selected_skill})

    module_name = SKILLS[selected_skill]["module"]
    module = importlib.import_module(module_name)
    result = module.run_skill(request, logger=logger, trace_id=trace_id)
    logger.log("orchestrator_result", {"trace_id": trace_id, "selected_skill": selected_skill, "result": result})

    # Persist generation results to database
    if "generation" in selected_skill:
        saved = STORE.save(result, trace_id=trace_id)
        logger.log("database_save", {"trace_id": trace_id, "question_id": result.get("question_id"), "saved": saved})

    return {"trace_id": trace_id, "selected_skill": selected_skill, "result": result, "log_path": str(logger.log_path), "database_path": str(STORE.db_path)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Route a math request to the correct skill")
    parser.add_argument("--request", default="Generate an easy arithmetic question")
    parser.add_argument("--json", default="", help="Optional JSON payload")
    args = parser.parse_args()

    if args.json:
        payload = json.loads(args.json)
    else:
        payload = {"prompt": args.request}

    print(json.dumps(process_request(payload), indent=2))
