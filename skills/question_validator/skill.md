# Question Validator Skill

## Description
Check whether a generated math question is solvable, unambiguous, and has a clear answer path.

## Routing Contract
The orchestrator should send only this description to the router LLM. When the request requires question validation, the orchestrator executes this skill.

## Expected Input
- topic
- question_text
- answer (optional)

## Expected Output
A structured payload with is_valid, reason, answer_present, and source skill.
