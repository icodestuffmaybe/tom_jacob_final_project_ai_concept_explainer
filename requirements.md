# AI Concept Explainer: POC Requirements Document

**Target Audience**: Grade 7-12 students (ages 12-18)  
**Subject Coverage**: General purpose across all academic subjects  
**Development Framework**: Claude Code Implementation Guide
**Deployment**: Single laptop/desktop computer  
**Version**: 1.0 POC  

## Executive Summary

The AI Concept Explainer POC is a web-based educational application that helps grade 7-12 students understand complex concepts through AI-powered explanations with source verification. The system uses the Feynman technique to ensure deep understanding, provides adaptive quizzes, and generates SVG visualizations for enhanced learning. This POC is designed to run entirely on a single commodity computer.

## Core Features Overview

### 1. Source-Verified AI Explanations
- Uses Gemini 2.5 Flash/Pro for cost-effective, high-quality explanations
- Real-time web search for credible sources (Wikipedia, arXiv, academic sites)
- Perplexity-style inline citations with numbered references
- Anti-hallucination through source grounding

### 2. Feynman Technique Implementation
- Step-by-step concept breakdown using simple language
- Student re-explanation interface
- Gap identification and targeted clarification
- Progressive simplification until mastery

### 3. Adaptive Quiz System
- Auto-generated questions based on explained concepts
- Difficulty adjustment based on student performance
- Immediate feedback with extended explanations
- Mastery tracking (85% accuracy threshold)

### 4. Visual Learning with SVG
- LLM-generated SVG flashcards using Gemini
- Minimalist, zen-inspired educational graphics
- Feynman technique integrated into visual design
- Dark background with chalk white text for optimal readability

### 5. Related Topic Discovery
- Automatic identification of prerequisite concepts
- Suggested next topics for deeper learning
- Cross-subject connections
- Personalized learning paths

## Technical Architecture

### Technology Stack

**Frontend:**
- **Framework**: React.js with TypeScript
- **Styling**: Tailwind CSS for responsive design
- **State Management**: React Context API (simpler than Redux for POC)
- **SVG Display**: Native SVG rendering with React components
- **Build Tool**: Vite for fast development

**Backend:**
- **Framework**: FastAPI (Python) for REST API
- **Web Server**: Uvicorn for ASGI
- **Task Queue**: Python threading for background tasks (simpler than Celery for POC)
- **Session Management**: JWT tokens with python-jose

**Database:**
- **Primary DB**: SQLite with SQLAlchemy ORM
- **Vector Store**: ChromaDB (embedded vector database for semantic search)
- **File Storage**: Local filesystem for uploaded content

**AI/ML Stack:**
- **LLM**: Google Gemini 2.5 Flash (primary) / Gemini 2.5 Pro (complex queries)
- **Web Search**: SerpAPI or Brave Search API for source retrieval
- **Embeddings**: Sentence-transformers (all-MiniLM-L6-v2) for semantic search
- **PDF Processing**: PyPDF2 for document parsing

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (React + TypeScript)          │
│  ┌─────────────┐ ┌─────────────┐ ┌──────────────────┐  │
│  │   Query     │ │   Learning  │ │    Progress      │  │
│  │   Input     │ │   Display   │ │    Dashboard     │  │
│  └─────────────┘ └─────────────┘ └──────────────────┘  │
└─────────────────────────┬───────────────────────────────┘
                          │ HTTP/WebSocket
┌─────────────────────────▼───────────────────────────────┐
│                 Backend API (FastAPI)                    │
│  ┌──────────────────────────────────────────────────┐   │
│  │            Request Handler & Router              │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌─────────────┐ ┌──────────────┐ ┌───────────────┐    │
│  │   Concept   │ │    Source    │ │     Quiz      │    │
│  │  Explainer  │ │  Verifier    │ │   Generator   │    │
│  └─────────────┘ └──────────────┘ └───────────────┘    │
│  ┌─────────────┐ ┌──────────────┐ ┌───────────────┐    │
│  │     SVG     │ │   Learning   │ │    Topic      │    │
│  │  Generator  │ │   Tracker    │ │  Recommender  │    │
│  └─────────────┘ └──────────────┘ └───────────────┘    │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│              External Services & Storage                 │
│  ┌──────────────┐ ┌───────────────┐ ┌──────────────┐   │
│  │ Gemini API   │ │  Web Search   │ │   SQLite     │   │
│  └──────────────┘ └───────────────┘ └──────────────┘   │
│  ┌──────────────┐ ┌───────────────┐                     │
│  │  ChromaDB    │ │  Local Files  │                     │
│  └──────────────┘ └───────────────┘                     │
└──────────────────────────────────────────────────────────┘
```

## Data Models

### SQLite Schema (SQLAlchemy Models)

```python
# models.py

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(String, primary_key=True)  # UUID
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    grade_level = Column(Integer)  # 7-12
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime)
    preferences = Column(JSON)  # Learning preferences
    
class Concept(Base):
    __tablename__ = 'concepts'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    subject = Column(String)
    description = Column(Text)
    prerequisites = Column(JSON)  # List of concept IDs
    related_topics = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class LearningSession(Base):
    __tablename__ = 'learning_sessions'
    
    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey('students.id'))
    concept_id = Column(String, ForeignKey('concepts.id'))
    query = Column(Text)
    explanation = Column(Text)
    sources = Column(JSON)  # List of source citations
    svg_diagrams = Column(JSON)  # List of SVG content
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
class Quiz(Base):
    __tablename__ = 'quizzes'
    
    id = Column(String, primary_key=True)
    session_id = Column(String, ForeignKey('learning_sessions.id'))
    questions = Column(JSON)  # Quiz questions and answers
    student_responses = Column(JSON)
    score = Column(Float)
    mastery_achieved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Progress(Base):
    __tablename__ = 'progress'
    
    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey('students.id'))
    concept_id = Column(String, ForeignKey('concepts.id'))
    mastery_level = Column(Float)  # 0-100%
    attempts = Column(Integer)
    last_reviewed = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow)
```

## API Endpoints

### Core API Structure

```python
# Main endpoints for Claude Code to implement

POST   /api/auth/register
POST   /api/auth/login
GET    /api/auth/me

# Concept Explanation
POST   /api/explain
       Body: { "query": string }
       Response: { 
         "explanation": string,
         "sources": [{ "title": string, "url": string, "snippet": string }],
         "svg_flashcard": string,
         "session_id": string
       }

# Feynman Technique
POST   /api/feynman/student-explanation
       Body: { "session_id": string, "explanation": string }
       Response: { 
         "gaps_identified": [string],
         "clarifications": string,
         "simplified_explanation": string
       }

# Quiz Generation
POST   /api/quiz/generate
       Body: { "session_id": string, "difficulty": string }
       Response: { 
         "quiz_id": string,
         "questions": [{ 
           "id": string,
           "question": string,
           "type": "multiple_choice" | "short_answer",
           "options": [string]?,
         }]
       }

POST   /api/quiz/submit
       Body: { "quiz_id": string, "answers": [{ "question_id": string, "answer": string }] }
       Response: { 
         "score": number,
         "feedback": [{ "question_id": string, "correct": boolean, "explanation": string }],
         "mastery_achieved": boolean
       }

# Progress Tracking  
GET    /api/progress
       Response: { "concepts": [{ "concept_id": string, "name": string, "mastery": number }] }

# Topic Recommendation
GET    /api/recommendations/{concept_id}
       Response: { 
         "prerequisites": [{ "id": string, "name": string }],
         "next_topics": [{ "id": string, "name": string, "reason": string }],
         "related": [{ "id": string, "name": string, "subject": string }]
       }
```

## Core Feature Implementation Requirements

### 1. RAG-Based Concept Explanation Engine

**Workflow Requirements:**

1. **Query Input**: Accept single text string from user (e.g., "What is photosynthesis?")

2. **Keyword Extraction**: 
   - Use LLM to extract 3-5 searchable keywords from the query
   - Focus on core concepts and technical terms
   - Example: "What is photosynthesis?" → ["photosynthesis", "plants", "chlorophyll", "sunlight"]

3. **Source Retrieval**:
   - Search Wikipedia API first for authoritative general knowledge
   - Perform web search using extracted keywords + "educational explanation"
   - Filter results for credible educational domains (.edu, .org, Khan Academy, etc.)
   - Limit to top 5 most relevant sources

4. **Content Processing**:
   - Summarize retrieved content using LLM
   - Extract key facts, definitions, and concepts
   - Create consolidated context for explanation generation

5. **Explanation Generation**:
   - If sources found: Generate explanation grounded in source content with citations
   - If no sources: Generate explanation from LLM knowledge, clearly marked as "general knowledge"
   - Apply Feynman technique: simple language, analogies, real-world examples

6. **Citation Formatting**:
   - Add numbered citations [1], [2] for source-based claims
   - Include source list with title, URL, and snippet

### 2. LLM-Powered SVG Flashcard Generation

**Requirements:**
- Use the provided prompt template for consistent, high-quality educational flashcards
- Canvas: 800x600 pixels with dark background (#1a1a1a)
- Content sections:
  - Concept title (centered top)
  - Core essence (what it really means)
  - Simple explanation (beginner-friendly)
  - Real-world example
  - Zen-inspired visual element
- Typography: Minimum 14px body text, 24px title, chalk white (#f0f0f0)
- Generate complete, valid SVG code via Gemini 2.5
- Fallback to simple text SVG if generation fails

### 3. Adaptive Quiz Generation

**Requirements:**
- Generate questions based on the explained concept
- Mix of question types: multiple choice (60%), short answer (40%)
- Difficulty levels: Easy, Medium, Hard
- Include explanations for both correct and incorrect answers
- Track attempts and adjust difficulty based on performance
- Mastery threshold: 85% accuracy over 3 attempts

### 4. Source Verification Service

**Wikipedia Integration:**
- Primary source for general knowledge
- Use Wikipedia API for search and content retrieval
- Extract page summaries (first 500 characters)
- Include Wikipedia URL for reference

**Web Search Integration:**
- Secondary source for additional context
- Use search API (Brave, SerpAPI, or similar)
- Filter for educational domains
- Credibility scoring based on domain authority

**Credibility Ranking:**
- Tier 1: Wikipedia, .edu, .gov sites
- Tier 2: Khan Academy, Britannica, educational .org sites
- Tier 3: Other credible educational sources
- Exclude: Forums, Q&A sites, user-generated content

### 5. Progress Tracking

**Requirements:**
- Track concepts learned per student
- Record mastery level (0-100%) for each concept
- Store quiz performance history
- Identify knowledge gaps and struggling areas
- Generate personalized learning recommendations
- Visual progress dashboard with charts

```python
# explanation_service.py

import google.generativeai as genai
from typing import List, Dict, Optional

class ExplanationService:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.search_client = SerpAPIClient(api_key=SERP_API_KEY)
        self.wikipedia_api = WikipediaAPI()
        
    async def explain_concept(self, query: str):
        # Step 1: Extract keywords from query
        keywords = await self.extract_keywords(query)
        
        # Step 2: Search for credible sources using keywords
        sources = await self.search_sources(keywords)
        
        # Step 3: Summarize search results
        if sources:
            source_summary = await self.summarize_sources(sources)
            # Step 4: Generate explanation with source context (RAG approach)
            explanation = await self.generate_explanation_with_sources(
                query, source_summary, sources
            )
        else:
            # Fallback: Generate explanation without sources
            explanation = await self.generate_explanation_without_sources(query)
            sources = []
        
        # Step 5: Generate SVG flashcard visualization
        svg_flashcard = await self.generate_svg_flashcard(query, explanation)
        
        # Step 6: Format response with citations
        formatted_response = self.format_with_citations(explanation, sources)
        
        return {
            "explanation": formatted_response,
            "sources": sources,
            "svg_flashcard": svg_flashcard
        }
    
    async def extract_keywords(self, query: str):
        prompt = f"""
        Extract 3-5 key search terms from this educational query:
        "{query}"
        
        Return only the keywords separated by commas, no explanation.
        Focus on the core concepts and technical terms.
        """
        
        response = self.model.generate_content(prompt)
        return response.text.strip().split(',')
    
    async def search_sources(self, keywords: list):
        sources = []
        
        # Search Wikipedia first
        for keyword in keywords[:2]:  # Limit to avoid too many API calls
            wiki_results = await self.wikipedia_api.search(keyword.strip())
            if wiki_results:
                sources.extend(wiki_results[:2])  # Take top 2 results
        
        # Search web for additional sources
        search_query = ' '.join(keywords)
        web_results = await self.search_client.search(
            search_query + " educational explanation"
        )
        
        # Filter for credible educational sources
        credible_sources = self.filter_credible_sources(web_results)
        sources.extend(credible_sources[:3])  # Take top 3 credible sources
        
        return sources[:5]  # Limit total sources to 5
    
    async def summarize_sources(self, sources: list):
        source_texts = []
        for source in sources:
            source_texts.append(f"Source: {source['title']}\n{source['snippet']}")
        
        prompt = f"""
        Summarize these educational sources into key facts and concepts:
        
        {chr(10).join(source_texts)}
        
        Extract the most important information that would help explain the topic.
        Focus on facts, definitions, and key concepts.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    async def generate_explanation_with_sources(self, query, source_summary, sources):
        prompt = f"""
        Explain this concept using the Feynman Technique: "{query}"
        
        Use this verified information from credible sources:
        {source_summary}
        
        Guidelines:
        1. Start with the core essence - what this really means
        2. Explain in simple terms a middle school student would understand
        3. Use analogies and real-world examples
        4. Break down complex ideas into smaller parts
        5. Include numbered citations [1], [2], etc. when referencing facts
        
        Structure your explanation with:
        - Brief introduction
        - Core explanation using simple language
        - Real-world example or analogy
        - Why this matters
        
        Keep the explanation concise but complete.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    async def generate_explanation_without_sources(self, query):
        prompt = f"""
        Explain this concept using the Feynman Technique: "{query}"
        
        Guidelines:
        1. Start with the core essence - what this really means
        2. Explain in simple terms a middle school student would understand
        3. Use analogies and real-world examples
        4. Break down complex ideas into smaller parts
        
        Structure your explanation with:
        - Brief introduction
        - Core explanation using simple language
        - Real-world example or analogy
        - Why this matters
        
        Note: Explain based on general knowledge without specific citations.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def filter_credible_sources(self, sources):
        credible_domains = [
            '.edu', '.gov', '.org', 
            'britannica.com', 'khanacademy.org', 
            'sciencedirect.com', 'nature.com',
            'mit.edu', 'stanford.edu', 'harvard.edu'
        ]
        
        credible = []
        for source in sources:
            if any(domain in source.get('url', '').lower() for domain in credible_domains):
                credible.append(source)
        
        return credible
```

### 2. SVG Flashcard Generation Service

The SVG generator creates beautiful, minimalist educational flashcards using LLM:

- **Design Philosophy**: Zen-inspired minimalism with matrix-style aesthetics
- **Content Structure**: Title, core essence, simple explanation, visual element
- **Color Scheme**: Dark background (#1a1a1a) with chalk white text (#f0f0f0)
- **Layout**: 800x600px canvas with golden ratio proportions
- **Feynman Integration**: Visual representation reinforces the simplified explanation

```python
# svg_generator.py

import google.generativeai as genai

class SVGGenerator:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
    async def generate_svg_flashcard(self, topic: str, explanation: str):
        # Extract core concepts from the explanation for the SVG
        core_essence = await self.extract_core_essence(topic, explanation)
        
        prompt = f"""
        Create a Minimalist Educational SVG Flashcard
        You are a minimalist designer who specializes in explaining complex concepts simply using the Feynman technique. 
        Create an SVG flashcard (800x600 pixels) that teaches the following concept:

        TOPIC: {topic}

        CORE EXPLANATION: {core_essence}

        Content Structure:
        - Concept Title - Center at the top
        - Core Essence - A brief, deep analysis of what the concept really means
        - Simple Explanation - Break it down like you're explaining to a beginner, using everyday language
        - Real-World Example - A concrete, relatable analogy or example
        - Visual Element - A simple, zen-inspired graphic that represents the concept

        Design Style:
        - Aesthetic: Futuristic matrix style combined with zen minimalism
        - Color Scheme: Dark background (#1a1a1a) with chalk white text (#f0f0f0) for contrast
        - Layout: Clean grid-based design using golden ratio proportions
        - Typography: Minimum 14px font size for body text, 24px for title
        - Spacing: Generous use of negative space for "breathability"
        - Visual Inspiration: Song dynasty painting mood - simple, elegant, meaningful

        Layout Requirements:
        - Canvas: 800x600 pixels with 20px margins
        - Title centered at top (y=50)
        - Core essence in upper section (y=120-180)
        - Central zen graphic (y=200-400) - simple, symbolic illustration
        - Simple explanation at bottom (y=420-520)
        - Balance all elements harmoniously

        IMPORTANT: Generate ONLY valid SVG code starting with <svg> and ending with </svg>.
        No markdown, no explanations, just the SVG code.
        """
        
        response = self.model.generate_content(prompt)
        svg_response = response.text
        
        # Clean the response to ensure only SVG content
        svg_content = self.clean_svg_response(svg_response)
        
        return svg_content
    
    async def extract_core_essence(self, topic: str, explanation: str):
        prompt = f"""
        From this explanation about "{topic}":
        {explanation[:500]}  # Limit to first 500 chars to keep it concise
        
        Extract:
        1. The single most important concept (one sentence)
        2. A simple analogy or real-world example
        3. Why this matters in everyday life
        
        Keep each point to one sentence maximum.
        """
        
        return await self.gemini_client.generate(
            prompt,
            model="gemini-2.5-flash"
        )
    
    def clean_svg_response(self, response: str):
        # Remove any markdown code blocks if present
        response = response.replace('```svg', '').replace('```', '')
        
        # Find the SVG content
        svg_start = response.find('<svg')
        svg_end = response.find('</svg>') + 6
        
        if svg_start != -1 and svg_end > svg_start:
            return response[svg_start:svg_end]
        
        # If no valid SVG found, return a fallback SVG
        return self.get_fallback_svg()
    
    def get_fallback_svg(self):
        return '''
        <svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
            <rect width="800" height="600" fill="#1a1a1a"/>
            <text x="400" y="50" font-size="24" fill="#f0f0f0" text-anchor="middle" font-family="Arial, sans-serif">
                Concept Loading...
            </text>
            <text x="400" y="300" font-size="16" fill="#f0f0f0" text-anchor="middle" font-family="Arial, sans-serif">
                Visual generation in progress
            </text>
        </svg>
        '''
```

### 3. Adaptive Quiz Generator

```python
# quiz_service.py

import google.generativeai as genai
import json

class QuizService:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
    async def generate_quiz(self, session: LearningSession, difficulty: str):
        prompt = f"""
        Generate a quiz based on this explanation:
        {session.explanation}
        
        Difficulty: {difficulty}
        
        Create 5 questions:
        - 3 multiple choice questions
        - 2 short answer questions
        
        Format as JSON:
        {{
            "questions": [
                {{
                    "question": "...",
                    "type": "multiple_choice",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "B",
                    "explanation": "..."
                }}
            ]
        }}
        """
        
        response = self.model.generate_content(prompt)
        return json.loads(response.text)
    
    def evaluate_answer(self, question, student_answer):
        # Evaluation logic with partial credit
        pass
```

### 4. Source Verification Service

```python
# source_verifier.py

class SourceVerifier:
    def __init__(self):
        self.wikipedia_api = WikipediaAPI()
        self.search_api = BraveSearchAPI()  # or SerpAPI
        
    async def search_and_verify(self, keywords: list):
        sources = []
        
        # Search Wikipedia for each keyword
        for keyword in keywords:
            try:
                wiki_results = await self.wikipedia_api.search(keyword.strip())
                if wiki_results:
                    # Get page content for better snippets
                    for result in wiki_results[:2]:
                        page_content = await self.wikipedia_api.get_page_summary(result['title'])
                        sources.append({
                            'title': result['title'],
                            'url': result['url'],
                            'snippet': page_content[:500],  # First 500 chars
                            'source_type': 'wikipedia'
                        })
            except Exception as e:
                print(f"Wikipedia search error for {keyword}: {e}")
        
        # General web search for additional educational content
        search_query = ' '.join(keywords) + " educational explanation"
        try:
            web_results = await self.search_api.search(search_query)
            
            # Filter and rank by credibility
            credible_sources = self.filter_credible_sources(web_results)
            
            for source in credible_sources[:3]:  # Top 3 credible sources
                sources.append({
                    'title': source.get('title', ''),
                    'url': source.get('url', ''),
                    'snippet': source.get('snippet', ''),
                    'source_type': 'web'
                })
        except Exception as e:
            print(f"Web search error: {e}")
        
        # Deduplicate and rank sources
        unique_sources = self.deduplicate_sources(sources)
        return self.rank_sources(unique_sources)[:5]  # Return top 5
    
    def filter_credible_sources(self, sources):
        # Educational and authoritative domains
        preferred_domains = [
            '.edu', '.gov', '.org',
            'khanacademy.org', 'britannica.com',
            'coursera.org', 'edx.org', 'mit.edu',
            'stanford.edu', 'harvard.edu', 'oxford.ac.uk',
            'cambridge.org', 'nature.com', 'sciencedirect.com',
            'nationalgeographic.com', 'smithsonianmag.com',
            'scientificamerican.com', 'nasa.gov'
        ]
        
        # Avoid these domains
        avoid_domains = [
            'quora.com', 'reddit.com', 'yahoo.com',
            'answers.com', 'ask.com'
        ]
        
        credible = []
        for source in sources:
            url = source.get('url', '').lower()
            
            # Skip if in avoid list
            if any(domain in url for domain in avoid_domains):
                continue
                
            # Prioritize educational domains
            if any(domain in url for domain in preferred_domains):
                source['credibility_score'] = 0.9
                credible.append(source)
            # Accept other .org and .edu sites
            elif '.edu' in url or '.org' in url:
                source['credibility_score'] = 0.7
                credible.append(source)
            # Accept other sources with lower priority
            else:
                source['credibility_score'] = 0.5
                credible.append(source)
        
        return sorted(credible, key=lambda x: x['credibility_score'], reverse=True)
    
    def deduplicate_sources(self, sources):
        seen_urls = set()
        unique = []
        
        for source in sources:
            url = source.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique.append(source)
        
        return unique
    
    def rank_sources(self, sources):
        # Rank by source type and credibility
        def get_rank_score(source):
            score = source.get('credibility_score', 0.5)
            if source.get('source_type') == 'wikipedia':
                score += 0.3  # Boost Wikipedia sources
            return score
        
        return sorted(sources, key=get_rank_score, reverse=True)


class WikipediaAPI:
    def __init__(self):
        self.base_url = "https://en.wikipedia.org/api/rest_v1"
        
    async def search(self, query: str):
        # Implementation for Wikipedia search
        # Returns list of {'title': str, 'url': str}
        pass
    
    async def get_page_summary(self, title: str):
        # Get page extract/summary
        # Returns first paragraph or summary text
        pass
```

## Frontend Components Structure

```typescript
// Component structure for Claude Code to implement

src/
├── components/
│   ├── QueryInput.tsx        // Main search/query interface
│   ├── ExplanationDisplay.tsx // Shows AI explanation with citations
│   ├── SourcePanel.tsx       // Expandable source citations
│   ├── SVGFlashcard.tsx      // Displays LLM-generated SVG flashcard
│   ├── QuizInterface.tsx     // Quiz questions and feedback
│   ├── ProgressDashboard.tsx // Student progress visualization
│   └── TopicRecommender.tsx  // Related topics suggestions
├── services/
│   ├── api.ts               // API client for backend
│   ├── auth.ts              // Authentication handling
│   └── storage.ts           // Local storage management
├── hooks/
│   ├── useExplanation.ts    // Custom hook for explanations
│   ├── useQuiz.ts           // Quiz state management
│   └── useProgress.ts       // Progress tracking
└── App.tsx                   // Main application component
```

## Development Guidelines for Claude Code

### Key Implementation Principles

1. **RAG-First Approach**: Always search for sources before generating explanations
2. **Graceful Fallbacks**: If sources unavailable, use LLM knowledge without citations
3. **Single Query Input**: Accept natural language queries without structured fields
4. **LLM for Visuals**: Use Gemini to generate complete SVG flashcards
5. **Caching Strategy**: Cache common queries to reduce API costs
6. **Error Handling**: Implement robust error handling for API failures

### Required Dependencies

**Backend (Python)**:
- FastAPI, Uvicorn (web framework)
- SQLAlchemy (ORM for SQLite)
- google-generativeai (Gemini API)
- wikipedia-api (Wikipedia integration)
- serpapi-python or similar (web search)
- python-jose (JWT authentication)
- httpx (async HTTP client)

**Frontend (React/TypeScript)**:
- Vite (build tool)
- React Router (navigation)
- Tailwind CSS (styling)
- Axios (API calls)
- React Markdown (rendering explanations)

### Environment Configuration

```env
GEMINI_API_KEY=your_gemini_api_key
SEARCH_API_KEY=your_search_api_key
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URL=sqlite:///./app.db
```

### Testing Strategy

1. Test with diverse queries across subjects
2. Verify citation accuracy
3. Validate SVG generation
4. Test fallback scenarios (no sources)
5. Ensure quiz difficulty adaptation works
6. Check progress tracking accuracy

### Example Complete Flow

```python
# Example of the complete explanation flow

async def handle_user_query(query: str):
    """
    Example: User asks "What is photosynthesis?"
    """
    
    # 1. Extract keywords: ["photosynthesis", "plants", "energy", "sunlight"]
    keywords = await extract_keywords(query)
    
    # 2. Search sources:
    # - Wikipedia: "Photosynthesis" article
    # - Educational sites: Khan Academy, Britannica
    sources = await search_sources(keywords)
    
    # 3. Summarize sources:
    # "Photosynthesis is the process by which plants convert sunlight, 
    #  water, and CO2 into glucose and oxygen..."
    summary = await summarize_sources(sources) if sources else None
    
    # 4. Generate explanation with Feynman technique:
    # "Imagine plants are like solar panels on a house. Just as solar panels
    #  capture sunlight to make electricity, plants capture sunlight to make
    #  their own food..."
    explanation = await generate_explanation(query, summary, sources)
    
    # 5. Generate SVG flashcard:
    # Creates a 800x600 minimalist visual with:
    # - Title: "Photosynthesis"
    # - Core essence: "How plants make food from sunlight"
    # - Simple graphic: Stylized plant with sun rays
    # - Key equation: CO2 + H2O + light → glucose + O2
    svg_flashcard = await generate_svg_flashcard(query, explanation)
    
    # 6. Format with citations:
    # "Plants use photosynthesis to convert sunlight into energy [1]. 
    #  This process takes place in chloroplasts [2]..."
    formatted_explanation = format_with_citations(explanation, sources)
    
    return {
        "explanation": formatted_explanation,
        "sources": sources,
        "svg_flashcard": svg_flashcard,
        "session_id": generate_session_id()
    }
```

### Sample Test Queries

```python
test_queries = [
    "What is photosynthesis and why is it important?",
    "Explain the Pythagorean theorem with a real-world example",
    "How does democracy work in modern societies?",
    "What caused World War I and its major consequences?",
    "Explain Newton's laws of motion with everyday examples",
    "What is the difference between DNA and RNA?",
    "How do supply and demand affect prices?",
    "What is climate change and what causes it?",
    "Explain the water cycle step by step",
    "How does the internet actually work?"
]
```

## Success Criteria for POC

### Core Functionality
- **Query Processing**: Single text input successfully extracts keywords and retrieves sources
- **RAG Implementation**: Wikipedia + web search results are summarized and used for explanations
- **Fallback Working**: System generates explanations without citations when no sources found
- **SVG Generation**: LLM creates valid 800x600px educational flashcards
- **Citation Format**: Inline numbered references [1], [2] correctly link to sources

### Performance Targets
- Explanation generation < 5 seconds
- SVG flashcard generation < 3 seconds
- Runs smoothly on 8GB RAM laptop
- SQLite handles 1000+ sessions

### Educational Quality
- Explanations use Feynman technique effectively
- Language appropriate for middle/high school students
- Sources are credible (Wikipedia, .edu, educational sites)
- Quiz questions align with explained content
- Visual flashcards reinforce key concepts

### User Experience
- Clean, intuitive interface
- Mobile-responsive design
- Clear source attribution
- Smooth quiz interaction
- Progress tracking works

## Next Steps After POC

1. **User Testing**: Test with 5-10 grade 7-12 students
2. **Feedback Integration**: Refine based on user feedback
3. **Performance Optimization**: Improve caching and API efficiency
4. **Content Enhancement**: Add more sophisticated SVG templates
5. **Feature Expansion**: Add voice input, collaborative features
6. **Deployment Planning**: Consider cloud deployment for wider access