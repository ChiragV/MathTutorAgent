import json
import os
import re
from typing import Any, Dict, Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

try:
    import openai
except Exception:  # pragma: no cover
    openai = None

try:
    from google import genai
except Exception:  # pragma: no cover
    genai = None

if load_dotenv:
    load_dotenv()


class LLMClient:
    """Generic LLM client that supports OpenAI and Gemini (Google) backends."""

    def __init__(self) -> None:
        self.provider = os.environ.get("LLM_PROVIDER", "openai").lower()
        self.client = None
        self.model = None

        if self.provider == "openai" and openai is not None:
            key = os.environ.get("OPENAI_API_KEY")
            self.model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
            if key:
                self.client = openai.OpenAI(api_key=key)

        if self.provider == "gemini" and genai is not None:
            key = os.environ.get("GEMINI_API_KEY")
            self.model = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
            if key:
                try:
                    self.client = genai.Client(api_key=key)
                except Exception:
                    self.client = None

    def generate_text(self, prompt: str, max_tokens: int = 256, logger=None, trace_id: str | None = None) -> str:
        """Generate text from the selected provider. Falls back to a deterministic stub."""
        if logger is not None:
            logger.log("llm_request", {"trace_id": trace_id, "prompt": prompt, "max_tokens": max_tokens})

        if self.provider == "openai" and self.client is not None:
            try:
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.2,
                )
                text = resp.choices[0].message.content.strip()
            except Exception:
                text = self.stub_generate_text(prompt)
            if logger is not None:
                logger.log("llm_response", {"trace_id": trace_id, "response": text})
            return text

        if self.provider == "gemini" and self.client is not None:
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )
                text = getattr(response, "text", None)
                text = (text or str(response)).strip()
                if logger is not None:
                    logger.log("llm_response", {"trace_id": trace_id, "response": text})
                return text
            except Exception as exc:
                text = self.stub_generate_text(prompt)
                if logger is not None:
                    logger.log("llm_response", {"trace_id": trace_id, "response": text, "fallback_reason": str(exc)})
                return text

        stub = self.stub_generate_text(prompt)
        if logger is not None:
            logger.log("llm_response", {"trace_id": trace_id, "response": stub})
        return stub

    def stub_generate_text(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        difficulty = self._extract_prompt_value(prompt, "difficulty", "easy").lower()

        if "router for a math tutor" in prompt_lower:
            return self._stub_route(prompt_lower)

        if "arithmetic question" in prompt_lower:
            return self._stub_arithmetic(difficulty)

        return json.dumps(
            {
                "question": "What is 2 + 3?",
                "answer": "5",
                "explanation": "Add 2 and 3 to get 5.",
                "hints": ["Start with the first number.", "Count up three more."],
            }
        )

    def _extract_prompt_value(self, prompt: str, key: str, default: str) -> str:
        match = re.search(rf"{key}:\s*([^.]+)", prompt, re.IGNORECASE)
        return match.group(1).strip() if match else default

    def _stub_route(self, prompt_lower: str) -> str:
        if any(term in prompt_lower for term in ("algebra", "equation", "variable")):
            skill = "algebra-generation"
        elif "fraction" in prompt_lower:
            skill = "fraction-generation"
        elif any(term in prompt_lower for term in ("geometry", "area", "perimeter", "volume")):
            skill = "geometry-generation"
        elif any(term in prompt_lower for term in ("word problem", "story")):
            skill = "word-problem-generation"
        elif any(term in prompt_lower for term in ("classify", "difficulty")):
            skill = "difficulty-classifier"
        elif any(term in prompt_lower for term in ("validate", "valid", "ambiguous")):
            skill = "question-validator"
        elif any(term in prompt_lower for term in ("duplicate", "similar")):
            skill = "duplicate-detector"
        else:
            skill = "arithmetic-generation"
        return json.dumps({"skill": skill, "reason": "Deterministic fallback route for local execution."})

    def _stub_arithmetic(self, difficulty: str) -> str:
        examples = {
            "easy": {
                "question": "What is 8 + 7?",
                "answer": "15",
                "explanation": "Add 8 and 7 to get 15.",
                "hints": ["Start at 8.", "Count up 7 more."],
            },
            "medium": {
                "question": "A box has 18 pencils. If 6 students share them equally, how many pencils does each student get?",
                "answer": "3",
                "explanation": "Divide 18 pencils by 6 students: 18 / 6 = 3.",
                "hints": ["Use division.", "Find how many groups of 6 fit into 18."],
            },
            "hard": {
                "question": "Compute 48 x 17 - 156.",
                "answer": "660",
                "explanation": "First multiply 48 x 17 = 816. Then subtract 156 to get 660.",
                "hints": ["Break 17 into 10 + 7.", "Subtract 156 after multiplying."],
            },
        }
        return json.dumps(examples.get(difficulty, examples["easy"]))

    def generate_question(self, prompt: str, logger=None, trace_id: str | None = None) -> Dict[str, Any]:
        raw = self.generate_text(prompt, logger=logger, trace_id=trace_id)
        return self.parse_generation(raw)

    def parse_generation(self, text: str) -> Dict[str, Any]:
        text = text.strip()
        json_text = text
        fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
        if fence_match:
            json_text = fence_match.group(1)

        try:
            payload = json.loads(json_text)
            if isinstance(payload, dict):
                return {
                    "question": str(payload.get("question") or payload.get("question_text") or ""),
                    "answer": str(payload.get("answer") or ""),
                    "explanation": str(payload.get("explanation") or payload.get("solution") or ""),
                    "hints": payload.get("hints") if isinstance(payload.get("hints"), list) else [],
                }
        except json.JSONDecodeError:
            pass

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        result: Dict[str, Any] = {"question": "", "answer": "", "explanation": "", "hints": []}
        current: Optional[str] = None

        for line in lines:
            low = line.lower()
            if low.startswith("question:"):
                current = "question"
                result["question"] = line.split(":", 1)[1].strip()
            elif low.startswith("answer:"):
                current = "answer"
                result["answer"] = line.split(":", 1)[1].strip()
            elif low.startswith("explanation:"):
                current = "explanation"
                result["explanation"] = line.split(":", 1)[1].strip()
            elif low.startswith("hints:"):
                current = "hints"
            elif current == "hints" and line.startswith("-"):
                result["hints"].append(line[1:].strip())
            else:
                if current and current in result:
                    result[current] = (result[current] + " " + line).strip()

        return result
