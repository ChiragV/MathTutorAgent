# Arithmetic Generation Skill

## Description
Generate arithmetic questions for addition, subtraction, multiplication, or division and return a structured question payload.

## Routing Contract
The orchestrator should send only this description to the router LLM. When the request requires arithmetic generation, the orchestrator executes this skill.

## Expected Input
- topic: arithmetic
- difficulty: easy, medium, or hard
- question_type: addition, subtraction, multiplication, division, or mixed

## Expected Output
A structured payload with question text, answer, solution, hints, and metadata.
