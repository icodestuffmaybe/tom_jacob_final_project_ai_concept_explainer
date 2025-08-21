import axios from 'axios'
import type { 
  Explanation, 
  Quiz, 
  QuizAnswer, 
  QuizResult 
} from '../types'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// No authentication interceptors needed for simple version

export const explanationAPI = {
  explainConcept: async (query: string): Promise<Explanation> => {
    const response = await api.post('/api/explain', { query })
    return response.data
  },

  getRecommendations: async (conceptId: string) => {
    const response = await api.get(`/api/recommendations/${conceptId}`)
    return response.data
  },
}

export const quizAPI = {
  generateQuiz: async (sessionId: string, difficulty: string = 'medium'): Promise<Quiz> => {
    const response = await api.post('/api/quiz/generate', {
      session_id: sessionId,
      difficulty,
    })
    return response.data
  },

  submitQuiz: async (quizId: string, answers: QuizAnswer[]): Promise<QuizResult> => {
    const response = await api.post('/api/quiz/submit', {
      quiz_id: quizId,
      answers,
    })
    return response.data
  },

  getQuiz: async (quizId: string) => {
    const response = await api.get(`/api/quiz/${quizId}`)
    return response.data
  },
}

export default api