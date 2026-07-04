from ollama import Client
from pydantic import BaseModel
from typing import Literal, Optional

Difficulty = Literal["easy", "medium", "hard"]
QuestionType = Literal["addition", "subtraction", "multiplication", "division", "mixed"]


class ArithmeticSkillRequest(BaseModel):
    topic: str = "arithmetic"
    difficulty: Difficulty = "hard"
    question_type: Optional[QuestionType] = None
    student_age: Optional[int] = None
    format: str = "open_ended"
    hints_requested: bool = False


class ArithmeticSkillResponse(BaseModel):
    question_id: str
    question_text: str
    difficulty: Difficulty
    answer: str
    solution: str
    topic: str
    question_type: QuestionType
    source_skill: str
    hints: list[str]
    metadata: dict


def test_arithmetic_generation_skill(
    model_name: str = "phi4-mini",
    host: str = "http://localhost:11434",
    request: Optional[ArithmeticSkillRequest] = None,
) -> ArithmeticSkillResponse:
    request = request or ArithmeticSkillRequest()

    prompt = (
        "You are the Arithmetic Generation skill for an adaptive math tutor. "
        "Generate one arithmetic question using the requested difficulty and question type. "
        "Return only valid JSON matching the output schema. "
        "Do not include any explanation outside the JSON object."
    )

    if request.question_type:
        prompt += f" Use question_type={request.question_type}."

    prompt += (
        " The response must include question_id, question_text, difficulty, answer, solution, "
        "topic, question_type, source_skill, hints, and metadata."
    )

    client = Client(host=host)

    response = client.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a math problem generator specialized in arithmetic."},
            {"role": "user", "content": prompt},
        ],
        format=ArithmeticSkillResponse.model_json_schema(),
    )

    return ArithmeticSkillResponse.model_validate_json(response.message.content)


if __name__ == "__main__":
    print("Connecting to local Ollama engine for Arithmetic Generation skill test...")

    sample_request = ArithmeticSkillRequest(
        difficulty="hard",
        question_type="addition",
        student_age=15,
        format="open_ended",
        hints_requested=True,
    )

    try:
        result = test_arithmetic_generation_skill(request=sample_request)
        print("\n✅ Skill test succeeded:\n")
        print(result.model_dump_json(indent=2))
    except Exception as exc:
        print("\n❌ Skill test failed:")
        print(exc)
        print("Ensure the Ollama engine is running locally on http://localhost:11434 and the model is available.")
