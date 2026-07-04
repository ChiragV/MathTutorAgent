# Math Tutor Agent - Quick Reference

## Architecture

- **Orchestrator** (`orchestrator.py`): Routes requests to appropriate skills based on the prompt
- **Skills**: Specialized modules for arithmetic, algebra, fractions, geometry, word problems, validation, and duplicate detection
- **Database** (`skills/database.py`): SQLite store for persistent question history
- **Logging** (`skills/common.py`): JSONL trace log at `logs/trace.jsonl` records all LLM requests/responses and skill execution
- **UI** (`ui/app.py`): FastAPI web interface

## Running the System

### CLI (Orchestrator)
```bash
# Generate an arithmetic question
python orchestrator.py --request "Generate an easy arithmetic question"

# Generate a specific type
python orchestrator.py --request "Generate a hard algebra question"
python orchestrator.py --request "Generate a geometry problem about area"
```

### Query the Database
```bash
# Show statistics
python query_store.py --stats

# Show recent questions
python query_store.py --recent 10

# Filter by topic
python query_store.py --recent 5 --topic arithmetic

# Find similar questions
python query_store.py --find-duplicates "What is 2 + 3?"
python query_store.py --find-duplicates "What is 2 + 3?" --topic arithmetic
```

### Web UI
```bash
uvicorn ui.app:app --reload
# Visit http://localhost:8000
```

## Data Storage

### Logs
- **Location**: `logs/trace.jsonl`
- **Format**: JSONL (one JSON entry per line)
- **Contents**: All LLM prompts, responses, skill selections, and outcomes
- **Use**: Debug what went into the LLM and what came out

### Database
- **Location**: `data/questions.db`
- **Schema**: 
  - `questions` table with fields: `question_id`, `topic`, `difficulty`, `question_text`, `answer`, `solution`, `source_skill`, `trace_id`, `created_at`
  - Indexes on `topic`, `difficulty`, and `question_text` for fast lookup
- **Use**: Query question history, find duplicates, analyze trends

## Skills

Each skill has:
- `skill.md`: Description sent to the router LLM
- `skill.py`: Implementation with `run_skill(request, logger, trace_id)` function
- `test_skill.py`: 3 test cases per skill

### Generation Skills
- **arithmetic-generation**: Addition, subtraction, multiplication, division
- **algebra-generation**: Equations and inequalities
- **fraction-generation**: Simplification, comparison, operations
- **geometry-generation**: Area, perimeter, volume
- **word-problem-generation**: Real-world scenarios

### Utility Skills
- **difficulty-classifier**: Verify question difficulty
- **question-validator**: Check if question is solvable and clear
- **duplicate-detector**: Find similar questions in database

## Troubleshooting

### Check what LLM received and returned
```bash
tail -f logs/trace.jsonl | grep -E 'llm_request|llm_response'
```

### Find all requests for a specific trace ID
```bash
grep 'trace_id.*abc123' logs/trace.jsonl
```

### See orchestrator routing decisions
```bash
grep 'orchestrator_selection' logs/trace.jsonl
```

### List all questions in a topic
```bash
python query_store.py --recent 100 --topic arithmetic
```
