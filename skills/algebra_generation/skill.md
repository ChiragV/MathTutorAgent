# Algebra Generation Skill

## Description
Generate algebra questions that ask the learner to solve for a variable, simplify an expression, or reason about an equation.

## Routing Contract
The orchestrator should send only this description to the router LLM. When the request requires algebra generation, the orchestrator executes this skill.

## Expected Input
- topic: algebra
- difficulty: easy, medium, or hard
- question_type: equation or inequality

## Expected Output
A structured question payload with question text, answer, solution, hints, and metadata.
