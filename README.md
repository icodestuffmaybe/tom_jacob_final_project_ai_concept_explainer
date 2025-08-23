# AI Concept Explainer - Student Capstone Exercise

A 20-hour capstone project for grade 7-12 students to implement core AI components in an educational application. Students will apply prompt engineering, RAG (Retrieval-Augmented Generation), and AI agents concepts from their 3-session AI course.

## Project Overview

This is a **complete, working educational platform** where students implement the **core AI intelligence** that powers the system. The database, API endpoints, frontend, and infrastructure are ready - students make it smart by implementing the AI components they learned about in class.

### What Students Will Implement

| Exercise | Session Topic | Component | Hours | Learning Focus |
|----------|---------------|-----------|-------|----------------|
| 1A | Prompt Engineering | Explanation Generation | 4 | Feynman Technique prompts |
| 1B | Prompt Engineering | Quiz Generation | 2 | JSON format prompts |
| 1C | Prompt Engineering | SVG Flashcards | 2 | Creative design prompts |
| 2A | RAG | Keyword Extraction | 2 | Query processing |
| 2B | RAG | Wikipedia Search | 4 | Content retrieval |
| 2C | RAG | Source Integration | 2 | Information synthesis |
| 3A | AI Agents | Student Evaluation | 2 | ReAct framework |
| 3B | AI Agents | Quiz Assessment | 2 | Performance analysis |

**Total: 20 hours** covering all course concepts with hands-on implementation.

## Features (When Complete)

- **RAG-Based Explanations**: Source-verified AI explanations using Wikipedia
- **Feynman Technique**: Step-by-step concept breakdown using simple language
- **Visual Learning**: AI-generated SVG flashcards with educational design
- **Adaptive Quizzes**: Auto-generated questions with difficulty adjustment
- **Progress Tracking**: Mastery tracking with 85% accuracy threshold
- **Agent-Based Assessment**: AI agents that evaluate student understanding

## Technology Stack

**Backend:**
- FastAPI (Python) - REST API
- SQLAlchemy - ORM for SQLite
- Google Gemini 2.5 - AI explanations and generation
- Wikipedia API - Source verification
- JWT Authentication

**Database:**
- SQLite - Local database
- Models: Student, Concept, LearningSession, Quiz, Progress

## Quick Start for Students

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Setup Instructions

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   # Create .env file in backend directory
   echo GEMINI_API_KEY=your_api_key_here > .env
   ```

5. **Test your setup:**
   ```bash
   python test_setup.py
   ```

### Running Tests

Test individual exercises as you implement them:

```bash
# Prompt Engineering (Session 1)
python test_exercise_1a_explanation.py
python test_exercise_1b_quiz.py

# RAG System (Session 2)  
python test_exercise_2a_keywords.py

# AI Agents (Session 3)
python test_exercise_3a_agent.py
```

### Running the Backend

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Required: Get from https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Database
DATABASE_URL=sqlite:///./app.db

# Security
JWT_SECRET_KEY=your-secure-secret-key
```

### API Key Setup

1. **Gemini API Key** (Required):
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add to your `.env` file

## Student Implementation Guide

### File Structure for Exercises

```
backend/app/
├── services/
│   ├── explanation_service.py  # Exercises 1A, 2A, 2B, 2C
│   ├── quiz_service.py         # Exercises 1B, 3B
│   └── svg_generator.py        # Exercise 1C
├── api/
│   └── explain.py              # Exercise 3A
└── ...
```

### Implementation Process

1. **Read the detailed instructions** in `student_guide.md`
2. **Look for TODO comments** in the code files - they contain step-by-step instructions
3. **Remove the assertion** when you start implementing each function
4. **Test frequently** using the provided test scripts

### Success Criteria

Students succeed when:
- All test scripts pass without assertion errors
- API endpoints return intelligent, relevant responses
- Full system integration works end-to-end
- They can explain their implementation using course concepts

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database Schema

### Core Models

- **Student**: User accounts with grade level and preferences
- **Concept**: Educational concepts with prerequisites and related topics
- **LearningSession**: Individual explanation sessions with sources and SVG
- **Quiz**: Generated quizzes with questions and student responses
- **Progress**: Mastery tracking per student per concept

## Project Structure

```
ai-concept-explainer-exercise/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes (some student implementation)
│   │   ├── core/          # Configuration (complete)
│   │   ├── database/      # Database setup (complete)
│   │   ├── models/        # SQLAlchemy models (complete)
│   │   ├── services/      # Business logic (STUDENT IMPLEMENTS)
│   │   └── main.py        # FastAPI app (complete)
│   └── requirements.txt
├── test_exercise_*.py     # Test scripts for each exercise
├── student_guide.md       # Detailed implementation guide
├── session*_course_notes.html  # Course reference materials
└── README.md             # This file
```

## Troubleshooting

### Common Issues

1. **"Assertion Error" when running tests**
   - This is expected! Remove the `assert False` line and implement the function

2. **"Gemini API not configured"**
   - Ensure `GEMINI_API_KEY` is set in `.env`
   - Verify API key is valid

3. **JSON parsing errors in quiz generation**
   - Check your prompt format specification
   - Ensure AI returns pure JSON without markdown

4. **Wikipedia search returns empty results**
   - Check URL encoding for special characters
   - Implement proper error handling

### Getting Help

1. **Read the TODO comments** in the code files
2. **Check `student_guide.md`** for detailed instructions
3. **Run test scripts** to see specific error messages

## Educational Goals

This capstone project teaches students to:

- **Apply prompt engineering techniques** in real applications
- **Build RAG systems** that retrieve and use external knowledge
- **Implement AI agents** that can reason and provide feedback
- **Work with professional codebases** and APIs
- **Handle errors and edge cases** in AI applications
- **Test and validate** AI system components

## Course Concept Mapping

### Session 1: Prompt Engineering
- **Persona prompting**: "You are an expert teacher..."
- **Few-shot learning**: Provide examples in prompts
- **Format specification**: Exact output structure requirements
- **Chain of thought**: "Let's think step by step"

### Session 2: RAG (Retrieval-Augmented Generation)
- **Query processing**: Extract meaningful search terms
- **Content retrieval**: Get relevant external information
- **Information synthesis**: Combine sources with AI knowledge
- **Quality control**: Validate and filter retrieved content

### Session 3: AI Agents
- **ReAct framework**: Reason → Act → Observe
- **Agent roles**: Specialized AI with specific responsibilities
- **Tool use**: Agents that can call functions and APIs
- **Evaluation patterns**: Agents that assess and provide feedback

## License

This project is designed for educational purposes as a capstone exercise.

## Support

For students:
- Check `student_guide.md` for detailed implementation instructions
- Use the test scripts to validate your implementations
- Ask TAs for help when stuck

---

**Built for AI education - helping students learn by building real applications**
