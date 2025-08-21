import React, { useState } from 'react'
import { explanationAPI } from '../services/api'
import type { Explanation } from '../types'

interface QueryInputProps {
  onExplanationReceived: (explanation: Explanation) => void
}

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
      const explanation = await explanationAPI.explainConcept(query.trim())
      onExplanationReceived(explanation)
      setQuery('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate explanation')
    } finally {
      setIsLoading(false)
    }
  }

  const exampleQueries = [
    "What is photosynthesis and why is it important?",
    "Explain the Pythagorean theorem with a real-world example",
    "How does democracy work in modern societies?",
    "What is climate change and what causes it?"
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
          {isLoading ? 'Generating Explanation...' : 'Explain This Concept'}
        </button>
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
              className="text-left p-2 text-sm bg-gray-800 hover:bg-gray-700 rounded border border-gray-600 hover:border-matrix-accent transition-colors disabled:opacity-50"
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