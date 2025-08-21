import React, { useState } from 'react'
import QueryInput from './components/QueryInput_simple'
import ExplanationDisplay from './components/ExplanationDisplay_simple'
import type { Explanation } from './types'
import './App.css'

const App: React.FC = () => {
  const [currentExplanation, setCurrentExplanation] = useState<Explanation | null>(null)

  return (
    <div className="min-h-screen bg-matrix-bg text-matrix-text">
      <nav className="border-b border-gray-700 p-4">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold matrix-text">AI Concept Explainer</h1>
          <div className="text-gray-400">
            <span className="text-sm">Educational AI Assistant</span>
          </div>
        </div>
      </nav>

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-matrix-text mb-4">
              Learn Any Concept with AI
            </h2>
            <p className="text-gray-400 text-lg">
              Ask questions about any topic and get clear explanations with visual aids and quizzes
            </p>
          </div>
          
          <QueryInput onExplanationReceived={setCurrentExplanation} />
          
          {currentExplanation && (
            <ExplanationDisplay explanation={currentExplanation} />
          )}

          {!currentExplanation && (
            <div className="zen-card rounded-lg p-8 text-center">
              <div className="text-6xl mb-4">🧠</div>
              <h3 className="text-xl font-semibold text-matrix-text mb-2">
                Ready to Learn?
              </h3>
              <p className="text-gray-400 mb-6">
                Type any question above to get started with AI-powered explanations
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div className="bg-gray-800 rounded p-4">
                  <h4 className="font-medium text-matrix-accent mb-2">📚 How it works</h4>
                  <p className="text-gray-300">
                    Ask any educational question and get explanations using the Feynman technique with verified sources.
                  </p>
                </div>
                <div className="bg-gray-800 rounded p-4">
                  <h4 className="font-medium text-matrix-accent mb-2">🎨 Visual Learning</h4>
                  <p className="text-gray-300">
                    Each explanation comes with an AI-generated visual flashcard to reinforce understanding.
                  </p>
                </div>
                <div className="bg-gray-800 rounded p-4">
                  <h4 className="font-medium text-matrix-accent mb-2">❓ Test Knowledge</h4>
                  <p className="text-gray-300">
                    Take adaptive quizzes to test your understanding and track your progress.
                  </p>
                </div>
                <div className="bg-gray-800 rounded p-4">
                  <h4 className="font-medium text-matrix-accent mb-2">🔍 Source Verified</h4>
                  <p className="text-gray-300">
                    All explanations are grounded in credible sources like Wikipedia and educational sites.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className="border-t border-gray-700 mt-16 py-8">
        <div className="container mx-auto px-4 text-center text-gray-400">
          <p>AI Concept Explainer - Educational AI Assistant</p>
          <p className="text-sm mt-2">Powered by Google Gemini AI</p>
        </div>
      </footer>
    </div>
  )
}

export default App