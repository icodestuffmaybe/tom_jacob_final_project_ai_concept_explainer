export interface User {
  id: string
  username: string
  email: string
  grade_level: number
  created_at: string
  last_active: string
}

export interface Source {
  title: string
  url: string
  snippet: string
  source_type: string
}

export interface Explanation {
  explanation: string
  sources: Source[]
  svg_flashcard: string
  session_id: string
  keywords: string[]
}

export interface Question {
  id: string
  question: string
  type: 'multiple_choice' | 'short_answer'
  options?: string[]
  correct_answer?: string
  sample_answer?: string
  explanation: string
}

export interface Quiz {
  quiz_id: string
  questions: Question[]
}

export interface QuizAnswer {
  question_id: string
  answer: string
}

export interface QuizFeedback {
  question_id: string
  correct: boolean
  explanation: string
  correct_answer?: string
  sample_answer?: string
  score?: number
}

export interface QuizResult {
  score: number
  feedback: QuizFeedback[]
  mastery_achieved: boolean
  correct_answers: number
  total_questions: number
}

export interface ConceptProgress {
  concept_id: string
  name: string
  subject: string
  mastery: number
  attempts: number
  last_reviewed: string
}

export interface ProgressStats {
  total_concepts_studied: number
  concepts_mastered: number
  mastery_percentage: number
  total_sessions: number
  recent_topics: Array<{
    query: string
    started_at: string
    session_id: string
  }>
}

// New chat-related types
export interface Message {
  id: string
  type: 'user' | 'assistant'
  content: string
  timestamp: Date
  svgContent?: string
  sources?: Source[]
  keywords?: string[]
  isError?: boolean
  isThinking?: boolean
  isQuiz?: boolean
  quizData?: {
    quizId: string
    questions: Question[]
  }
  metadata?: {
    expectingQuizAnswer?: boolean
    expectingTopicSelection?: boolean
    expectingQuizAnswers?: boolean
    sessionId?: string
    quizId?: string
    questions?: Question[]
    topics?: string[]
    lastTopic?: string
  }
}

export interface StreamingStep {
  id: string
  type: 'processing' | 'keywords' | 'sources' | 'explanation' | 'visual' | 'finalizing' | 'quiz' | 'grading' | 'topics'
  content: string
  brief?: string
  status: 'active' | 'completed' | 'error'
  timestamp: Date
}