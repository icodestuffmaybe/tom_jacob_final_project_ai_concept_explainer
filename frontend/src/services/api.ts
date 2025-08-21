import axios from 'axios'
import type { 
  User, 
  Explanation, 
  Quiz, 
  QuizAnswer, 
  QuizResult, 
  ConceptProgress, 
  ProgressStats 
} from '../types'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  register: async (userData: {
    username: string
    email: string
    password: string
    grade_level: number
  }) => {
    const response = await api.post('/api/auth/register', userData)
    return response.data
  },

  login: async (username: string, password: string) => {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    
    const response = await api.post('/api/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/api/auth/me')
    return response.data
  },
}

export const explanationAPI = {
  explainConcept: async (query: string): Promise<Explanation> => {
    const response = await api.post('/api/explain', { query })
    return response.data
  },

  processStudentExplanation: async (sessionId: string, explanation: string) => {
    const response = await api.post('/api/feynman/student-explanation', {
      session_id: sessionId,
      explanation,
    })
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

export const progressAPI = {
  getProgress: async (): Promise<{ concepts: ConceptProgress[] }> => {
    const response = await api.get('/api/progress')
    return response.data
  },

  getProgressStats: async (): Promise<ProgressStats> => {
    const response = await api.get('/api/progress/stats')
    return response.data
  },

  getConceptProgress: async (conceptId: string) => {
    const response = await api.get(`/api/progress/concept/${conceptId}`)
    return response.data
  },
}

export default api