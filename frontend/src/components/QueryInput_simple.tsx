import React, { useState } from 'react'
import axios from 'axios'
import type { Explanation } from '../types'

interface QueryInputProps {
  onExplanationReceived: (explanation: Explanation) => void
}

const API_BASE_URL = 'http://localhost:8000'

const QueryInput: React.FC<QueryInputProps> = ({ onExplanationReceived }) => {
  const [query, setQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setIsLoading(true)
    setError('')

    try {
      // Add timeout for long requests (60 seconds)
      const response = await axios.post(`${API_BASE_URL}/api/explain`, {
        query: query.trim()
      }, {
        timeout: 60000 // 60 seconds
      })
      
      onExplanationReceived(response.data)
      setQuery('')
    } catch (err: any) {
      if (err.code === 'ECONNABORTED') {
        setError('Request timed out. The AI is taking longer than expected. Please try again with a simpler question.')
      } else {
        setError(err.response?.data?.detail || 'Failed to generate explanation')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const exampleQueries = [
    "What is photosynthesis and why is it important?",
    "Explain the Pythagorean theorem with a real-world example",
    "How does democracy work in modern societies?",
    "What is climate change and what causes it?",
    "How do computers process information?",
    "What is DNA and how does it work?"
  ]

  return (
    <div className="zen-card rounded-lg p-6">
      <h2 className="text-2xl font-bold text-center matrix-text mb-6">
        Ask Me Anything
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask me to explain any concept... (e.g., 'What is photosynthesis?')"
            rows={3}
            className="w-full p-4 bg-gray-800 text-matrix-text rounded-lg border border-gray-600 focus:border-matrix-accent focus:outline-none resize-none"
            disabled={isLoading}
          />
        </div>

        {error && (
          <div className="text-red-400 text-sm">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="w-full py-3 px-4 bg-matrix-accent text-black rounded-lg hover:bg-green-400 disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
        >
          {isLoading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-black mr-2"></div>
              Generating AI Explanation...
            </div>
          ) : 'Explain This Concept'}
        </button>
        
        {isLoading && (
          <div className="text-center text-sm text-gray-400 mt-2">
            <p>🧠 AI is thinking... This may take 10-30 seconds</p>
            <p className="text-xs mt-1">Searching sources, generating explanation & visual aids</p>
          </div>
        )}
      </form>

      <div className="mt-6">
        <h3 className="text-sm font-semibold text-gray-400 mb-3">
          Try these example questions:
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {exampleQueries.map((example, index) => (
            <button
              key={index}
              onClick={() => setQuery(example)}
              disabled={isLoading}
              className="text-left p-3 text-sm bg-gray-800 hover:bg-gray-700 rounded border border-gray-600 hover:border-matrix-accent transition-colors disabled:opacity-50"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

export default QueryInput