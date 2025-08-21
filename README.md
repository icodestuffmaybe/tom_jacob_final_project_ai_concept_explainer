# AI Concept Explainer

A proof-of-concept educational application that helps grade 7-12 students understand complex concepts through AI-powered explanations with source verification, interactive quizzes, and visual learning aids.

## 🎯 Features

- **🌊 Real-Time Streaming**: Watch AI thinking process step-by-step in real-time
- **💬 ChatGPT-Style Interface**: Natural conversation flow with intelligent context awareness
- **RAG-Based Explanations**: Source-verified AI explanations using Wikipedia and educational websites
- **Feynman Technique**: Step-by-step concept breakdown using simple language
- **Visual Learning**: AI-generated SVG flashcards with zen-inspired design
- **Adaptive Quizzes**: Auto-generated questions with difficulty adjustment
- **Progress Tracking**: Mastery tracking with 85% accuracy threshold
- **Related Topics**: Automatic discovery of prerequisite and next concepts
- **🎨 Smooth Animations**: Enhanced UX with loading indicators and visual feedback

## 🏗️ Architecture

### Technology Stack

**Backend:**
- FastAPI (Python) - REST API
- SQLAlchemy - ORM for SQLite
- Google Gemini 2.5 - AI explanations and SVG generation
- Wikipedia API - Primary source verification
- JWT Authentication

**Frontend:**
- React 18 + TypeScript
- Vite - Build tool
- Tailwind CSS - Styling
- Axios - API client

**Database:**
- SQLite - Local database
- Models: Student, Concept, LearningSession, Quiz, Progress

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API key

### Super Quick Start (Recommended for Prototype)

#### 🌊 **Streaming Mode (Recommended)**
1. **Run the streaming chat interface:**
   ```cmd
   start_streaming.bat
   ```
   Features real-time AI thinking process visualization!

2. **Open your browser to:** http://localhost:5173

3. **Watch the AI work in real-time** as it processes your questions!

#### 🚀 **Simple Mode**
1. **Run basic version:**
   ```cmd
   start_simple.bat
   ```
   Clean interface without streaming effects.

**No registration required for either mode!**

### Backend Setup

#### Option 1: Quick Start (Windows)
1. **Run the startup script:**
   ```cmd
   start_backend.bat
   ```
   This will automatically create the virtual environment, install dependencies, and start the server.

#### Option 2: Manual Setup
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
   copy .env.example .env  # Windows
   # cp .env.example .env  # macOS/Linux
   # Edit .env and add your GEMINI_API_KEY
   ```

5. **Run the backend:**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at: http://localhost:8000

### Frontend Setup

#### Option 1: Quick Start (Windows)
1. **Run the startup script:**
   ```cmd
   start_frontend.bat
   ```
   This will automatically install dependencies and start the development server.

#### Option 2: Manual Setup
1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

   The app will be available at: http://localhost:5173

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Required: Get from https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: For enhanced source verification
SEARCH_API_KEY=your_search_api_key_here

# Database
DATABASE_URL=sqlite:///./app.db

# Security
JWT_SECRET_KEY=your-secure-secret-key
```

### API Keys Setup

1. **Gemini API Key** (Required):
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add to your `.env` file

2. **Search API Key** (Optional):
   - For enhanced source verification
   - Supports SerpAPI, Brave Search API, etc.

## 📖 Usage

### Basic Workflow

1. **Register/Login**: Create a student account
2. **Ask Questions**: Type any educational query
3. **Review Explanation**: Read AI-generated explanation with sources
4. **View Visual Aid**: Check the generated SVG flashcard
5. **Take Quiz**: Test understanding with adaptive questions
6. **Track Progress**: Monitor mastery levels and learning stats

### Example Queries

- "What is photosynthesis and why is it important?"
- "Explain the Pythagorean theorem with a real-world example"
- "How does democracy work in modern societies?"
- "What is climate change and what causes it?"

## 🧪 Development

### Backend Development

```bash
cd backend

# Run with auto-reload
uvicorn app.main:app --reload

# Run tests
pytest

# Check code style
black app/
flake8 app/
```

### Frontend Development

```bash
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Lint code
npm run lint

# Type checking
npx tsc --noEmit
```

### API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 Database Schema

### Core Models

- **Student**: User accounts with grade level and preferences
- **Concept**: Educational concepts with prerequisites and related topics
- **LearningSession**: Individual explanation sessions with sources and SVG
- **Quiz**: Generated quizzes with questions and student responses
- **Progress**: Mastery tracking per student per concept

## 🎨 Design Philosophy

### Educational Approach
- **Feynman Technique**: Explains complex concepts in simple terms
- **Source Verification**: Grounds explanations in credible sources
- **Progressive Learning**: Builds knowledge systematically
- **Visual Reinforcement**: SVG flashcards enhance understanding

### UI/UX Design
- **Matrix-Inspired**: Dark theme with green accents
- **Zen Minimalism**: Clean, focused interface
- **Mobile-Responsive**: Works on all device sizes
- **Accessibility**: High contrast and readable fonts

## 📋 Project Structure

```
ai-concept-explainer/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Configuration
│   │   ├── database/      # Database setup
│   │   ├── models/        # SQLAlchemy models
│   │   ├── services/      # Business logic
│   │   └── main.py        # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom hooks
│   │   ├── services/      # API client
│   │   ├── types/         # TypeScript types
│   │   └── main.tsx       # Entry point
│   └── package.json
├── requirements.md        # Detailed requirements
├── .env.example          # Environment template
└── README.md
```

## 🔍 Testing

### Sample Test Queries

Test the system with these educational queries:
- Science: "Explain photosynthesis", "What is DNA?"
- Math: "Pythagorean theorem", "What are prime numbers?"
- History: "Causes of World War I", "How democracy works"
- Physics: "Newton's laws of motion", "What is gravity?"

### Performance Targets

- Explanation generation: < 5 seconds
- SVG flashcard generation: < 3 seconds
- Quiz creation: < 3 seconds
- Runs on 8GB RAM laptop
- Handles 1000+ learning sessions

## 🚨 Troubleshooting

### Common Issues

1. **"Gemini API not configured"**
   - Ensure `GEMINI_API_KEY` is set in `.env`
   - Verify API key is valid

2. **Database errors**
   - Delete `app.db` to reset database
   - Check SQLite permissions

3. **CORS errors**
   - Verify frontend runs on port 5173
   - Check backend CORS configuration

4. **Import errors**
   - Ensure virtual environment is activated
   - Install requirements: `pip install -r requirements.txt`

### Development Tips

- Use browser dev tools to monitor API calls
- Check backend logs for detailed error messages
- Ensure both frontend and backend are running
- Test with simple queries first

## 📚 Educational Impact

### Learning Outcomes

- **Concept Mastery**: 85% accuracy threshold ensures deep understanding
- **Source Literacy**: Students learn to verify information
- **Visual Learning**: SVG flashcards reinforce key concepts
- **Self-Assessment**: Quizzes provide immediate feedback
- **Progress Awareness**: Dashboard shows learning journey

### Feynman Technique Implementation

1. **Simple Explanation**: AI breaks down complex concepts
2. **Identify Gaps**: Quiz results highlight knowledge gaps
3. **Simplify Further**: Adaptive explanations for struggling areas
4. **Use Analogies**: Real-world examples enhance understanding

## 🛠️ Future Enhancements

### Planned Features (Post-POC)

- Voice input/output support
- Collaborative learning features
- Advanced analytics dashboard
- Multi-language support
- Mobile app version
- Integration with LMS platforms

### Scalability Considerations

- PostgreSQL for production database
- Redis for caching
- Docker containerization
- Cloud deployment (AWS/GCP)
- CDN for static assets

## 📄 License

This project is a proof-of-concept for educational purposes.

## 🤝 Contributing

This is a POC project. For production development:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation at `/docs`
- Ensure all environment variables are configured
- Verify API keys are valid and have proper permissions

---

**Built with ❤️ for education and powered by AI**