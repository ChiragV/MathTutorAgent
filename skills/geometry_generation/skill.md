# Geometry Generation Skill

## Description
Generate geometry questions about area, perimeter, volume, or shape properties.

## Routing Contract
The orchestrator should send only this description to the router LLM. When the request requires geometry generation, the orchestrator executes this skill.

## Expected Input
- topic: geometry
- difficulty: easy, medium, or hard
- question_type: area, perimeter, or volume

## Expected Output
A structured question payload with question text, answer, solution, hints, and metadata.
