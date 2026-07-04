# Difficulty Classifier Skill

## Description
Assess whether a generated question matches the requested difficulty level and return a confidence score with rationale.

## Routing Contract
The orchestrator should send only this description to the router LLM. When the request requires difficulty classification, the orchestrator executes this skill.

## Expected Input
- topic
- difficulty
- question_text

## Expected Output
A structured payload with difficulty, confidence, reason, and source skill.
