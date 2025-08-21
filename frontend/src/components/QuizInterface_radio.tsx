import React, { useState } from 'react'
import type { Question } from '../types'

interface QuizInterfaceProps {
  questions: Question[]
  onSubmit: (answers: Record<string, string>) => void
  isLoading?: boolean
}

const QuizInterface: React.FC<QuizInterfaceProps> = ({ questions, onSubmit, isLoading = false }) => {
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({})

  const handleAnswerSelect = (questionId: string, answer: string) => {
    setSelectedAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }))
  }

  const handleSubmit = () => {
    onSubmit(selectedAnswers)
  }

  const allAnswered = questions.every(q => selectedAnswers[q.id])

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-xl font-semibold text-matrix-text mb-2">
          📝 Quiz Time!
        </h3>
        <p className="text-gray-400">
          Select the best answer for each question
        </p>
      </div>

      <div className="space-y-6">
        {questions.map((question, index) => (
          <div key={question.id} className="bg-gray-800 rounded-lg p-6 border border-gray-600">
            <h4 className="font-medium text-matrix-text mb-4 text-lg">
              {index + 1}. {question.question}
            </h4>

            {question.type === 'multiple_choice' && question.options && (
              <div className="space-y-3">
                {question.options.map((option, optionIndex) => {
                  const letter = String.fromCharCode(65 + optionIndex) // A, B, C, D
                  const isSelected = selectedAnswers[question.id] === option
                  
                  return (
                    <label 
                      key={optionIndex}
                      className={`
                        flex items-center p-3 rounded-lg border-2 cursor-pointer transition-all duration-200
                        ${isSelected 
                          ? 'border-matrix-accent bg-matrix-accent/10 text-matrix-accent' 
                          : 'border-gray-600 hover:border-gray-500 text-gray-300'
                        }
                      `}
                    >
                      <input
                        type="radio"
                        name={question.id}
                        value={option}
                        checked={isSelected}
                        onChange={(e) => handleAnswerSelect(question.id, e.target.value)}
                        className="sr-only" // Hide the default radio button
                      />
                      
                      {/* Custom radio button */}
                      <div className={`
                        w-5 h-5 rounded-full border-2 mr-3 flex items-center justify-center transition-all duration-200
                        ${isSelected 
                          ? 'border-matrix-accent bg-matrix-accent' 
                          : 'border-gray-500'
                        }
                      `}>
                        {isSelected && (
                          <div className="w-2 h-2 rounded-full bg-black"></div>
                        )}
                      </div>
                      
                      {/* Option letter and text */}
                      <div className="flex items-center">
                        <span className={`
                          font-bold mr-3 text-sm px-2 py-1 rounded
                          ${isSelected 
                            ? 'bg-matrix-accent text-black' 
                            : 'bg-gray-700 text-gray-300'
                          }
                        `}>
                          {letter}
                        </span>
                        <span className="flex-1">{option}</span>
                      </div>
                    </label>
                  )
                })}
              </div>
            )}

            {/* Progress indicator for this question */}
            <div className="mt-3 text-right">
              {selectedAnswers[question.id] ? (
                <span className="text-xs text-matrix-accent">✓ Answered</span>
              ) : (
                <span className="text-xs text-gray-500">⏳ Waiting for answer</span>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Progress summary */}
      <div className="bg-gray-800 rounded-lg p-4 border border-gray-600">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-400">Progress:</span>
          <span className="text-sm text-matrix-accent">
            {Object.keys(selectedAnswers).length}/{questions.length} answered
          </span>
        </div>
        
        <div className="w-full bg-gray-700 rounded-full h-2">
          <div 
            className="bg-matrix-accent h-2 rounded-full transition-all duration-300"
            style={{ 
              width: `${(Object.keys(selectedAnswers).length / questions.length) * 100}%` 
            }}
          ></div>
        </div>
      </div>

      {/* Submit button */}
      <div className="text-center">
        <button
          onClick={handleSubmit}
          disabled={!allAnswered || isLoading}
          className="px-8 py-3 bg-matrix-accent text-black rounded-lg hover:bg-green-400 disabled:opacity-50 disabled:cursor-not-allowed font-semibold text-lg transition-colors"
        >
          {isLoading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-black mr-2"></div>
              Evaluating Answers...
            </div>
          ) : (
            `Submit Quiz (${Object.keys(selectedAnswers).length}/${questions.length})`
          )}
        </button>
        
        {!allAnswered && (
          <p className="text-sm text-gray-400 mt-2">
            Please answer all questions before submitting
          </p>
        )}
      </div>
    </div>
  )
}

export default QuizInterface