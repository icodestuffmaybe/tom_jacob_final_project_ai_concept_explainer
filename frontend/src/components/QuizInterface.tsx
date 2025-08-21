import React, { useState, useEffect } from 'react'
import { quizAPI } from '../services/api'
import type { Quiz, QuizAnswer, QuizResult, Question } from '../types'

interface QuizInterfaceProps {
  sessionId: string
}

const QuizInterface: React.FC<QuizInterfaceProps> = ({ sessionId }) => {
  const [quiz, setQuiz] = useState<Quiz | null>(null)
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [result, setResult] = useState<QuizResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [difficulty, setDifficulty] = useState('medium')

  const generateQuiz = async () => {
    setIsGenerating(true)
    try {
      const newQuiz = await quizAPI.generateQuiz(sessionId, difficulty)
      setQuiz(newQuiz)
      setAnswers({})
      setResult(null)
    } catch (error) {
      console.error('Failed to generate quiz:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  const handleAnswerChange = (questionId: string, answer: string) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }))
  }

  const submitQuiz = async () => {
    if (!quiz) return

    setIsLoading(true)
    try {
      const quizAnswers: QuizAnswer[] = Object.entries(answers).map(([questionId, answer]) => ({
        question_id: questionId,
        answer
      }))

      const quizResult = await quizAPI.submitQuiz(quiz.quiz_id, quizAnswers)
      setResult(quizResult)
    } catch (error) {
      console.error('Failed to submit quiz:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const renderQuestion = (question: Question, index: number) => {
    const userAnswer = answers[question.id] || ''

    return (
      <div key={question.id} className="bg-gray-800 rounded-lg p-4 border border-gray-600">
        <h3 className="font-medium text-matrix-text mb-3">
          {index + 1}. {question.question}
        </h3>

        {question.type === 'multiple_choice' ? (
          <div className="space-y-2">
            {question.options?.map((option, optionIndex) => (
              <label key={optionIndex} className="flex items-center cursor-pointer">
                <input
                  type="radio"
                  name={question.id}
                  value={option}
                  checked={userAnswer === option}
                  onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                  className="mr-3"
                  disabled={!!result}
                />
                <span className="text-gray-300">{option}</span>
              </label>
            ))}
          </div>
        ) : (
          <textarea
            value={userAnswer}
            onChange={(e) => handleAnswerChange(question.id, e.target.value)}
            placeholder="Type your answer here..."
            rows={3}
            disabled={!!result}
            className="w-full p-3 bg-gray-700 text-matrix-text rounded border border-gray-600 focus:border-matrix-accent focus:outline-none disabled:opacity-50"
          />
        )}

        {result && (
          <div className="mt-3">
            {(() => {
              const feedback = result.feedback.find(f => f.question_id === question.id)
              if (!feedback) return null

              return (
                <div className={`p-3 rounded ${feedback.correct ? 'bg-green-900/30 border border-green-600' : 'bg-red-900/30 border border-red-600'}`}>
                  <div className="flex items-center mb-2">
                    <span className="mr-2">{feedback.correct ? '✅' : '❌'}</span>
                    <span className="font-medium">
                      {feedback.correct ? 'Correct!' : 'Incorrect'}
                    </span>
                  </div>
                  
                  {feedback.correct_answer && (
                    <p className="text-sm text-gray-300 mb-2">
                      <strong>Correct answer:</strong> {feedback.correct_answer}
                    </p>
                  )}
                  
                  {feedback.sample_answer && (
                    <p className="text-sm text-gray-300 mb-2">
                      <strong>Sample answer:</strong> {feedback.sample_answer}
                    </p>
                  )}
                  
                  <p className="text-sm text-gray-300">
                    {feedback.explanation}
                  </p>
                </div>
              )
            })()}
          </div>
        )}
      </div>
    )
  }

  if (!quiz) {
    return (
      <div className="text-center space-y-4">
        <div className="text-4xl mb-4">🧠</div>
        <h3 className="text-xl font-semibold text-matrix-text">Test Your Understanding</h3>
        <p className="text-gray-400 mb-6">
          Take a quiz to reinforce your learning and check your mastery of this concept.
        </p>
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-400 mb-2">
            Choose difficulty level:
          </label>
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            className="px-3 py-2 bg-gray-800 text-matrix-text rounded border border-gray-600 focus:border-matrix-accent focus:outline-none"
            disabled={isGenerating}
          >
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>
        
        <button
          onClick={generateQuiz}
          disabled={isGenerating}
          className="px-6 py-3 bg-matrix-accent text-black rounded-lg hover:bg-green-400 disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
        >
          {isGenerating ? 'Generating Quiz...' : 'Generate Quiz'}
        </button>
      </div>
    )
  }

  if (result) {
    const masteryMessage = result.mastery_achieved 
      ? "🎉 Excellent! You've mastered this concept!"
      : result.score >= 70 
        ? "👏 Good work! You're getting there."
        : "📚 Keep studying - you'll get it next time!"

    return (
      <div className="space-y-6">
        <div className="text-center zen-card rounded-lg p-6">
          <div className="text-4xl mb-4">
            {result.mastery_achieved ? '🎉' : result.score >= 70 ? '👏' : '📚'}
          </div>
          <h3 className="text-2xl font-bold text-matrix-text mb-2">Quiz Complete!</h3>
          <p className="text-lg text-gray-300 mb-4">{masteryMessage}</p>
          
          <div className="flex justify-center space-x-8 mb-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-matrix-accent">{result.score.toFixed(0)}%</div>
              <div className="text-sm text-gray-400">Score</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-matrix-accent">
                {result.correct_answers}/{result.total_questions}
              </div>
              <div className="text-sm text-gray-400">Correct</div>
            </div>
          </div>
          
          <button
            onClick={() => {
              setQuiz(null)
              setResult(null)
              setAnswers({})
            }}
            className="px-4 py-2 bg-gray-700 text-matrix-text rounded hover:bg-gray-600"
          >
            Try Again
          </button>
        </div>

        <div className="space-y-4">
          <h4 className="text-lg font-semibold text-matrix-text">Review Your Answers:</h4>
          {quiz.questions.map((question, index) => renderQuestion(question, index))}
        </div>
      </div>
    )
  }

  const allAnswered = quiz.questions.every(q => answers[q.id]?.trim())

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-xl font-semibold text-matrix-text mb-2">
          Quiz - {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)} Level
        </h3>
        <p className="text-gray-400">
          Answer all questions to test your understanding
        </p>
      </div>

      <div className="space-y-4">
        {quiz.questions.map((question, index) => renderQuestion(question, index))}
      </div>

      <div className="text-center">
        <button
          onClick={submitQuiz}
          disabled={!allAnswered || isLoading}
          className="px-6 py-3 bg-matrix-accent text-black rounded-lg hover:bg-green-400 disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
        >
          {isLoading ? 'Submitting...' : 'Submit Quiz'}
        </button>
      </div>
    </div>
  )
}

export default QuizInterface