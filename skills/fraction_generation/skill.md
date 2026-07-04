# Fraction Generation Skill

## Description
Generate fraction questions such as simplification, comparison, or addition with fractions.

## Routing Contract
The orchestrator should send only this description to the router LLM. When the request requires fraction generation, the orchestrator executes this skill.

## Expected Input
- topic: fractions
- difficulty: easy, medium, or hard
- question_type: simplification, comparison, or addition

## Expected Output
A structured question payload with question text, answer, solution, hints, and metadata.
