import os
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
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.2,
            )
            try:
                text = resp.choices[0].message.content.strip()
            except Exception:
                text = str(resp)
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
                text = str(exc)
                if logger is not None:
                    logger.log("llm_response", {"trace_id": trace_id, "response": text})
                return text

        stub = self.stub_generate_text(prompt)
        if logger is not None:
            logger.log("llm_response", {"trace_id": trace_id, "response": stub})
        return stub

    def stub_generate_text(self, prompt: str) -> str:
        return (
            "Question: What is 2 + 3?\n"
            "Answer: 5\n"
            "Explanation: Add 2 and 3 to get 5.\n"
            "Hints:\n- Start with the first number.\n- Count up three more.\n"
        )

    def generate_question(self, prompt: str, logger=None, trace_id: str | None = None) -> Dict[str, Any]:
        raw = self.generate_text(prompt, logger=logger, trace_id=trace_id)
        return self.parse_generation(raw)

    def parse_generation(self, text: str) -> Dict[str, Any]:
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
