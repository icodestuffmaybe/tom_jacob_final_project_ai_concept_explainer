# AI Concept Explainer - Student Exercise Guide

Welcome to your 20-hour capstone project! You'll be implementing the core AI components that make the AI Concept Explainer intelligent, applying everything you learned in the 3-session course.

## Project Overview

You're working with a **complete, professional codebase** - a working AI educational platform. Your job is to implement the **core AI intelligence** that powers the system. The database, API endpoints, frontend, and infrastructure are all ready - you just need to make it smart!

### What You'll Implement

| Exercise | Session | Component | Time | Core Learning |
|----------|---------|-----------|------|---------------|
| **1A** | Prompt Engineering | Explanation Generation | 4h | Feynman Technique prompts |
| **1B** | Prompt Engineering | Quiz Generation | 2h | JSON format prompts |
| **1C** | Prompt Engineering | SVG Flashcards | 2h | Creative design prompts |
| **2A** | RAG | Keyword Extraction | 2h | Query processing |
| **2B** | RAG | Wikipedia Search | 4h | Content retrieval |
| **2C** | RAG | Source Integration | 2h | Information synthesis |
| **3A** | AI Agents | Student Evaluation | 2h | ReAct framework |
| **3B** | AI Agents | Quiz Assessment | 2h | Performance analysis |

---

## Getting Started

### 1. Setup Your Environment

```bash
# 1. Navigate to the project directory
cd ai-concept-explainer-exercise

# 2. Set up the backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. Configure your API key
# Create a .env file in the backend directory
echo GEMINI_API_KEY=your_api_key_here > .env

# 4. Test your setup
python test_setup.py
```

### 2. Understand the Project Structure

```
ai-concept-explainer/
├── backend/
│   ├── app/
│   │   ├── services/           # YOU IMPLEMENT THESE
│   │   │   ├── explanation_service.py  # Exercises 1A, 2A, 2B, 2C
│   │   │   ├── quiz_service.py         # Exercise 1B, 3B
│   │   │   └── svg_generator.py        # Exercise 1C
│   │   ├── api/                # YOU IMPLEMENT PARTS OF THESE
│   │   │   └── explain.py              # Exercise 3A
│   │   ├── models/             # ALREADY COMPLETE
│   │   ├── database/           # ALREADY COMPLETE
│   │   └── core/               # ALREADY COMPLETE
│   └── requirements.txt
├── test_exercise_*.py          # YOUR TEST SCRIPTS
├── student_guide.md            # THIS FILE
```

### 3. Run Your First Test

```bash
# Test any exercise to see the current state
python test_exercise_1a_explanation.py

# You should see an assertion error - this means you need to implement it!
```

---

## Exercise Instructions

### Session 1: Prompt Engineering (8 hours)

Apply the prompt engineering techniques you learned to create intelligent AI interactions.

#### **Exercise 1A: Explanation Generation (4 hours)**
**File:** `backend/app/services/explanation_service.py`
**Function:** `generate_explanation_with_sources()`

**What you're building:** An AI prompt that generates educational explanations using the Feynman Technique.

**Key techniques to apply:**
- **Persona prompting:** "You are an expert educational AI..."
- **Clear instructions:** Step-by-step explanation structure
- **Format specification:** How to include citations [1], [2]
- **Integration:** Use the `source_summary` for RAG

**Success criteria:**
- Generates clear, simple explanations
- Uses middle school level language
- Includes real-world examples/analogies
- Includes citations from sources
- Follows Feynman Technique structure

**Test your work:**
```bash
python test_exercise_1a_explanation.py
```

#### **Exercise 1B: Quiz Generation (2 hours)**
**File:** `backend/app/services/quiz_service.py`
**Function:** `generate_quiz()`

**What you're building:** An AI prompt that creates multiple choice quizzes in JSON format.

**Key techniques to apply:**
- **Format specification:** Exact JSON structure required
- **Clear requirements:** 5 questions, 4 options each
- **Difficulty adaptation:** Easy/medium/hard variations
- **Validation:** Ensure correct answers are in options

**Success criteria:**
- Generates exactly 5 multiple choice questions
- Each question has 4 options
- Correct answers are valid options
- Returns proper JSON format
- Questions based on explanation content

**Test your work:**
```bash
python test_exercise_1b_quiz.py
```

#### **Exercise 1C: SVG Flashcard Generation (2 hours)**
**File:** `backend/app/services/svg_generator.py`
**Function:** `generate_svg_flashcard()`

**What you're building:** An AI prompt that creates educational SVG flashcards.

**Key techniques to apply:**
- **Persona prompting:** "You are a minimalist designer..."
- **Detailed specifications:** Size, colors, layout requirements
- **Creative constraints:** Zen-inspired, educational design
- **Output format:** Pure SVG code only

**Success criteria:**
- Generates valid SVG code (800x600 pixels)
- Uses dark theme (#1a1a1a background, #f0f0f0 text)
- Includes educational content about the topic
- Has clean, minimalist design
- No markdown formatting, just SVG

**Test your work:**
```bash
python test_exercise_1c_svg.py
```

---

### Session 2: RAG Implementation (8 hours)

Build a Retrieval-Augmented Generation system that finds and uses external knowledge.

#### **Exercise 2A: Keyword Extraction (2 hours)**
**File:** `backend/app/services/explanation_service.py`
**Function:** `extract_keywords()`

**What you're building:** Smart keyword extraction for Wikipedia searches.

**Key concepts to apply:**
- **Query processing:** Break down educational questions
- **Search optimization:** Terms that work with Wikipedia
- **Fallback strategies:** Handle cases without API
- **Educational focus:** Academic and learning-relevant terms

**Success criteria:**
- Extracts 3-5 relevant keywords
- Includes original query concept
- Uses Wikipedia-searchable terms
- Works without API (intelligent fallback)
- Focuses on educational concepts

**Test your work:**
```bash
python test_exercise_2a_keywords.py
```

#### **Exercise 2B: Wikipedia Search & Retrieval (4 hours)**
**File:** `backend/app/services/explanation_service.py`
**Function:** `search_wikipedia()`

**What you're building:** Wikipedia content retrieval and processing.

**Key concepts to apply:**
- **API integration:** Wikipedia REST API calls
- **Content extraction:** Get relevant article summaries
- **Error handling:** Handle missing articles gracefully
- **Data processing:** Clean and structure retrieved content

**Success criteria:**
- Successfully retrieves Wikipedia articles
- Handles both direct page hits and search results
- Extracts clean, relevant content snippets
- Returns structured data format
- Graceful error handling for missing content

**Test your work:**
```bash
python test_exercise_2b_wikipedia.py
```

#### **Exercise 2C: Source Integration & Summarization (2 hours)**
**File:** `backend/app/services/explanation_service.py`
**Function:** `summarize_sources()`

**What you're building:** Multi-source content synthesis for AI prompts.

**Key concepts to apply:**
- **Information synthesis:** Combine multiple sources
- **Content summarization:** Extract key facts and concepts
- **Context preparation:** Format for AI consumption
- **Quality filtering:** Focus on educational content

**Success criteria:**
- Combines multiple source texts effectively
- Extracts key educational concepts
- Creates coherent summary for AI prompts
- Maintains source attribution
- Filters for relevance and quality

**Test your work:**
```bash
python test_exercise_2c_sources.py
```

---

### Session 3: AI Agents (4 hours)

Implement intelligent agents that can reason, evaluate, and provide feedback.

#### **Exercise 3A: Student Evaluation Agent (2 hours)**
**File:** `backend/app/api/explain.py`
**Function:** `process_student_explanation()`

**What you're building:** A ReAct agent that evaluates student learning.

**Key concepts to apply:**
- **ReAct framework:** Thought → Action → Observation
- **Agent roles:** Educational evaluator and tutor
- **Structured reasoning:** Step-by-step analysis
- **Constructive feedback:** Help students improve

**Success criteria:**
- Uses ReAct pattern explicitly
- Compares student vs. correct explanations
- Identifies specific knowledge gaps
- Provides constructive clarifications
- Returns structured response format

**Test your work:**
```bash
python test_exercise_3a_agent.py
```

#### **Exercise 3B: Quiz Assessment Agent (2 hours)**
**File:** `backend/app/services/quiz_service.py`
**Function:** `evaluate_quiz()` (enhance existing)

**What you're building:** An intelligent quiz grading and feedback system.

**Key concepts to apply:**
- **Automated assessment:** Grade multiple choice answers
- **Performance analysis:** Calculate scores and mastery
- **Adaptive feedback:** Provide detailed explanations
- **Learning analytics:** Track progress patterns

**Success criteria:**
- Accurately grades quiz responses
- Calculates meaningful performance metrics
- Provides detailed feedback per question
- Determines mastery level (85% threshold)
- Handles edge cases (incomplete responses)

**Test your work:**
```bash
python test_exercise_3b_assessment.py
```

---

## Testing Your Work

### Individual Exercise Tests

Each exercise has its own test script:

```bash
# Prompt Engineering (Session 1)
python test_exercise_1a_explanation.py
python test_exercise_1b_quiz.py
python test_exercise_1c_svg.py

# RAG System (Session 2)
python test_exercise_2a_keywords.py
python test_exercise_2b_wikipedia.py
python test_exercise_2c_sources.py

# AI Agents (Session 3)
python test_exercise_3a_agent.py
python test_exercise_3b_assessment.py
```

### Full System Test

Once you've implemented all exercises:

```bash
# Start the backend
cd backend
python -m uvicorn app.main:app --reload

# In another terminal, run the full system test
python test_full_system.py
```

### Frontend Integration Test

```bash
# Start both backend and frontend
start_backend.bat
start_frontend.bat

# Test the complete application at http://localhost:5173
```

---

## Implementation Tips

### General Approach

1. **Read the TODO comments carefully** - they contain detailed instructions
2. **Remove the assertion** once you start implementing
3. **Test frequently** using the provided test scripts
4. **Check the TA guide** if you get stuck
5. **Ask for help** - TAs are there to support you!

### Prompt Engineering Best Practices

```python
# Good prompt structure
prompt = f"""
You are an expert educational AI.

Task: Explain {topic} using the Feynman Technique.

Requirements:
- Use simple language
- Include analogies
- Add citations [1], [2]

Source information: {sources}

Format:
1. What it is (simple definition)
2. How it works (mechanism)  
3. Real example (analogy)
4. Why it matters (importance)
"""

# Poor prompt structure
prompt = f"Explain {topic}"
```

### RAG Implementation Tips

```python
# Good Wikipedia search
async def search_wikipedia(self, keyword: str):
    try:
        # Direct page lookup first
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{keyword}"
        response = await client.get(url)
        if response.status_code == 200:
            return process_wikipedia_data(response.json())
        
        # Fallback to search API
        # ... search implementation
    except Exception as e:
        print(f"Error: {e}")
        return []

# Poor error handling
def search_wikipedia(self, keyword):
    url = f"https://en.wikipedia.org/wiki/{keyword}"
    response = requests.get(url)  # No error handling!
    return response.text  # Raw HTML!
```

### Agent Implementation Tips

```python
# Good ReAct agent
prompt = f"""
You are an educational evaluation agent.

THOUGHT: I need to compare these explanations systematically.
ACTION: I will identify gaps, misconceptions, and areas for improvement.
OBSERVATION: I will provide constructive feedback to help learning.

Original: {original_explanation}
Student: {student_explanation}

Analysis:
GAPS: [specific missing concepts]
CLARIFICATIONS: [what needs clarification]
SIMPLIFIED: [simpler explanation]
"""

# Poor agent design
prompt = f"Is this explanation correct? {student_explanation}"
```

---

## Common Issues & Solutions

### Issue: Assertion Error on First Run
**Solution:** This is normal! Remove the assertion and implement the function.

### Issue: JSON Parsing Error in Quiz Generation
**Solution:** Check your prompt format. The AI must return pure JSON without markdown.

### Issue: Wikipedia API Returns 404
**Solution:** Try URL encoding the keyword and implement search fallback.

### Issue: Empty or Invalid API Responses
**Solution:** Check your API key and prompt structure. Add better error handling.

### Issue: Agent Responses Not Parsing Correctly
**Solution:** Make your output format requirements very explicit in the prompt.

---

## Learning Resources

### Session 1 Review: Prompt Engineering
- **Persona prompting:** "You are a [role]..."
- **Few-shot learning:** Provide 2-3 examples
- **Chain of thought:** "Let's think step by step"
- **Format specification:** Exact output structure

### Session 2 Review: RAG
- **Retrieval:** Find relevant external information
- **Augmentation:** Enhance AI prompts with retrieved content
- **Generation:** Create responses using both AI knowledge and sources
- **Quality control:** Filter and validate sources

### Session 3 Review: AI Agents
- **ReAct framework:** Reason → Act → Observe
- **Tool use:** Agents can call functions and APIs
- **Multi-agent workflows:** Specialized agents working together
- **Evaluation patterns:** Critic agents that assess quality

---

## Grading Criteria

Your work will be evaluated on:

### Technical Implementation (40%)
- All functions implemented correctly
- Tests pass successfully
- Code follows best practices
- Error handling implemented

### Course Concept Application (30%)
- Proper use of prompt engineering techniques
- Effective RAG implementation
- Correct agent patterns and reasoning

### System Integration (20%)
- Components work together seamlessly
- API endpoints function correctly
- Frontend integration successful
- Database operations work

### Code Quality & Documentation (10%)
- Clean, readable code
- Appropriate comments
- Professional implementation
- Good error messages

---

## Getting Help

### Self-Help Resources
1. **Test scripts** - Run these first to see what's not working
2. **TODO comments** - Read them carefully for detailed instructions
3. **TA guide** - Check for common solutions and FAQs
4. **Course notes** - Review the session materials

### Ask for Help When:
- Tests are failing after multiple attempts
- You're getting unexpected API responses
- You're unsure about the prompt engineering approach
- The system integration isn't working

### How to Ask for Help:
1. **Run the test script** and share the error output
2. **Show your implementation** so TAs can see your approach
3. **Explain what you expected** vs what actually happened
4. **Mention which session concept** you're trying to apply

---

## Success Indicators

You'll know you're succeeding when:

- **Test scripts pass** without assertion errors
- **API responses look intelligent** and relevant
- **Full system test works** end-to-end
- **Frontend shows your AI responses** correctly
- **You can explain your approach** using course concepts

Remember: This is a **capstone project** that demonstrates your mastery of prompt engineering, RAG, and AI agents. Take your time, test frequently, and don't hesitate to ask for help!

Good luck!

---

*Built for AI education*
