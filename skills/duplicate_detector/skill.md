# Duplicate Detector Skill

## Description
Check whether a newly generated question duplicates an earlier question or is too similar to a prior item.

## Routing Contract
The orchestrator should send only this description to the router LLM. When the request requires duplicate detection, the orchestrator executes this skill.

## Expected Input
- topic
- question_text
- history (optional)

## Expected Output
A structured payload with is_duplicate, similarity_score, reason, and source skill.
