# Adaptive Math Tutor using Agent Skills, Memory, and Evaluation-Driven Development

## 1. Project Title
Adaptive Math Tutor using Agent Skills, Memory, and Evaluation-Driven Development

## 2. Project Goal
Build an agentic application that generates age-appropriate math questions while leveraging an Agent Skills architecture. The system should generate questions, validate them, adapt difficulty levels, avoid duplicates, track learner progress, and improve over time through evaluation and memory.

## 3. Core Concept
Instead of building one large Math Tutor agent, create a single orchestrator agent with multiple specialized skills. Each skill owns one responsibility and can be independently tested, evaluated, and improved.

## 4. Target Users
- Students
- Parents
- Teachers
- Homeschooling programs
- Test preparation learners

## 5. Primary Requirements

### 5.1 Question Generation
- Generate math questions on demand
- Support multiple topics
- Allow selection of difficulty level
- Generate answer and explanation
- Generate hints when requested

### 5.2 Difficulty Levels
- Easy
- Medium
- Hard

### 5.3 Math Domains
- Arithmetic
- Fractions
- Decimals
- Algebra
- Geometry
- Word Problems
- Percentages
- Ratios
- Probability
- SAT/Competitive Exam style questions

## 6. Long-Term Memory
The system should store:
- Previously generated questions
- Previously asked questions
- Student performance history
- Difficulty trends
- Skill evaluation results

The system should prevent:
- Duplicate questions
- Near-duplicate questions
- Repeated practice unless intentionally requested

## 7. Skills Architecture

### 7.1 Core Skills

#### Skill 1: Arithmetic Generation
Generate addition, subtraction, multiplication, and division questions.

#### Skill 2: Fraction Generation
Generate fraction questions and solutions.

#### Skill 3: Algebra Generation
Generate algebra equations and solutions.

#### Skill 4: Geometry Generation
Generate geometry-related questions.

#### Skill 5: Word Problem Generation
Generate real-world math word problems.

#### Skill 6: Difficulty Classifier
Verify that generated questions match the requested difficulty level.

#### Skill 7: Question Validator
Validate that:
- The question is solvable
- Exactly one answer exists
- The question is not ambiguous

#### Skill 8: Answer Validator
Verify generated answers using deterministic calculations.

#### Skill 9: Duplicate Detection
Search memory and identify duplicate or highly similar questions.

#### Skill 10: Hint Generator
Generate progressive hints without exposing the full solution.

#### Skill 11: Learner Analytics
Track:
- Weak areas
- Strong areas
- Improvement trends
- Recommended next topic

#### Skill 12: Adaptive Difficulty Manager
Increase or decrease difficulty based on performance.

#### Skill 13: Evaluation Manager
Run skill evaluations and quality checks.

### 7.2 Stretch Goal Skills

#### Skill 14: Skill Creator
Observe recurring workflows and propose new skills.

#### Skill 15: Skill Improver
Analyze failed evaluations and suggest improvements.

## 8. System Workflow

### 8.1 Question Generation Flow
User Request
→ Skill Router
→ Topic Generation Skill
→ Question Validator
→ Answer Validator
→ Duplicate Checker
→ Memory Store
→ Deliver Question

### 8.2 Student Response Flow
Student Answer
→ Answer Evaluation
→ Learner Analytics
→ Difficulty Adjustment
→ Next Question Recommendation

## 9. Memory Design

### 9.1 Question Table
- Question ID
- Topic
- Difficulty
- Question Text
- Answer
- Solution
- Created Date

### 9.2 Question History Table
- Student ID
- Question ID
- Date Asked
- Result
- Response Time

### 9.3 Student Profile Table
- Student ID
- Preferred Topics
- Skill Levels
- Mastered Concepts
- Weak Concepts

### 9.4 Evaluation Results Table
- Skill Name
- Evaluation Date
- Pass Rate
- Failure Categories

## 10. Evaluation-Driven Development
Each skill must include:
- Positive test cases
- Negative test cases
- Expected outputs
- Success criteria

Example evaluation:

Input:
Generate easy algebra question

Expected Skill:
algebra-generation

Expected Output:
- One variable
- Easy difficulty
- Single valid solution

## 11. Proposed Architecture

### 11.1 Frontend
- Web UI
- Chat-style interface

### 11.2 Backend
- Python
- FastAPI

### 11.3 Agent Framework
- LangGraph or similar orchestration framework

### 11.4 Database
- SQLite initially
- Support migration to PostgreSQL

### 11.5 Vector Store
- Optional
- Store question embeddings for duplicate detection

## 12. Project Folder Structure
```text
math-agent/
agents/
  orchestrator/
skills/
  arithmetic_generation/
  fraction_generation/
  algebra_generation/
  geometry_generation/
  word_problem_generation/
  difficulty_classifier/
  question_validator/
  answer_validator/
  duplicate_detector/
  hint_generator/
  learner_analytics/
  adaptive_difficulty/
  evaluation_manager/
memory/
  questions.db
  student_profiles.db
evals/
  arithmetic/
  algebra/
  geometry/
  fractions/
references/
  difficulty_rules/
  curriculum_rules/
assets/
  templates/
tests/
docs/
```

## 13. Capstone Deliverables

### Phase 1
- Generate questions
- Store questions
- Prevent duplicates

### Phase 2
- Skill-based architecture
- Difficulty management
- Question validation

### Phase 3
- Learner analytics
- Adaptive difficulty

### Phase 4
- Evaluation framework
- Skill performance dashboards

### Phase 5 (Stretch Goal)
- Self-improving skill system
- Automatic skill creation
- Automatic skill optimization

## 14. Non-Functional Requirements
- Modular skill architecture
- Pluggable skills
- Portable across AI platforms
- Testable skills
- Evaluation-first development
- Scalable memory management
- Skill versioning
- Skill ownership and governance

## 15. Success Criteria
- 95%+ valid question generation rate
- Zero duplicate questions served to the same learner
- Accurate difficulty classification
- Adaptive learning path recommendations
- Ability to add new math domains by adding new skills without modifying existing skills

## 16. Expected Outcome
An Agent Skills-based Adaptive Math Tutor that demonstrates:
- Modular skills architecture
- Long-term memory
- Evaluation-driven development
- Skill composition
- Adaptive learning
- Self-improving agent concepts

This project should serve as a practical demonstration of Agent Skills, procedural memory, evaluation frameworks, orchestration, and memory-driven agentic applications.
