# Word Problem Generation Skill

## Description
Generate contextual word problems that require converting a real-world scenario into a math question.

## Routing Contract
The orchestrator should send only this description to the router LLM. When the request requires word problem generation, the orchestrator executes this skill.

## Expected Input
- topic: word-problems
- difficulty: easy, medium, or hard
- question_type: shopping, comparison, or daily-life

## Expected Output
A structured question payload with question text, answer, solution, hints, and metadata.
