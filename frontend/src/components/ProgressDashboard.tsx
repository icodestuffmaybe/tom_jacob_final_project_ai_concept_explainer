import React, { useState, useEffect } from 'react'
import { progressAPI } from '../services/api'
import type { ConceptProgress, ProgressStats } from '../types'

const ProgressDashboard: React.FC = () => {
  const [progress, setProgress] = useState<ConceptProgress[]>([])
  const [stats, setStats] = useState<ProgressStats | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadProgress()
  }, [])

  const loadProgress = async () => {
    try {
      const [progressData, statsData] = await Promise.all([
        progressAPI.getProgress(),
        progressAPI.getProgressStats()
      ])
      setProgress(progressData.concepts)
      setStats(statsData)
    } catch (error) {
      console.error('Failed to load progress:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const getMasteryColor = (mastery: number) => {
    if (mastery >= 85) return 'text-green-400'
    if (mastery >= 70) return 'text-yellow-400'
    return 'text-red-400'
  }

  const getMasteryBadge = (mastery: number) => {
    if (mastery >= 85) return { emoji: '🎯', label: 'Mastered' }
    if (mastery >= 70) return { emoji: '📈', label: 'Learning' }
    return { emoji: '📚', label: 'Studying' }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-matrix-text text-xl">Loading progress...</div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-matrix-text mb-2">Learning Progress</h1>
        <p className="text-gray-400">Track your concept mastery and learning journey</p>
      </div>

      {/* Stats Overview */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="zen-card rounded-lg p-6 text-center">
            <div className="text-2xl font-bold text-matrix-accent mb-2">
              {stats.total_concepts_studied}
            </div>
            <div className="text-sm text-gray-400">Concepts Studied</div>
          </div>

          <div className="zen-card rounded-lg p-6 text-center">
            <div className="text-2xl font-bold text-green-400 mb-2">
              {stats.concepts_mastered}
            </div>
            <div className="text-sm text-gray-400">Concepts Mastered</div>
          </div>

          <div className="zen-card rounded-lg p-6 text-center">
            <div className="text-2xl font-bold text-matrix-accent mb-2">
              {stats.mastery_percentage.toFixed(0)}%
            </div>
            <div className="text-sm text-gray-400">Mastery Rate</div>
          </div>

          <div className="zen-card rounded-lg p-6 text-center">
            <div className="text-2xl font-bold text-matrix-accent mb-2">
              {stats.total_sessions}
            </div>
            <div className="text-sm text-gray-400">Learning Sessions</div>
          </div>
        </div>
      )}

      {/* Recent Topics */}
      {stats?.recent_topics && stats.recent_topics.length > 0 && (
        <div className="zen-card rounded-lg p-6">
          <h2 className="text-xl font-semibold text-matrix-text mb-4 flex items-center">
            <span className="mr-2">📚</span>
            Recent Learning Sessions
          </h2>
          <div className="space-y-3">
            {stats.recent_topics.map((topic, index) => (
              <div key={index} className="flex items-center justify-between py-2 border-b border-gray-700 last:border-b-0">
                <div>
                  <div className="text-matrix-text font-medium">{topic.query}</div>
                  <div className="text-sm text-gray-400">
                    {new Date(topic.started_at).toLocaleDateString()}
                  </div>
                </div>
                <div className="text-matrix-accent text-sm">
                  Session #{topic.session_id.slice(-6)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Concepts Progress */}
      <div className="zen-card rounded-lg p-6">
        <h2 className="text-xl font-semibold text-matrix-text mb-6 flex items-center">
          <span className="mr-2">🎯</span>
          Concept Mastery Progress
        </h2>

        {progress.length === 0 ? (
          <div className="text-center py-8">
            <div className="text-4xl mb-4">📖</div>
            <p className="text-gray-400 mb-4">No concepts studied yet</p>
            <p className="text-sm text-gray-500">
              Start learning by asking questions on the main page!
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {progress.map((concept) => {
              const badge = getMasteryBadge(concept.mastery)
              return (
                <div
                  key={concept.concept_id}
                  className="bg-gray-800 rounded-lg p-4 border border-gray-600 hover:border-gray-500 transition-colors"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center">
                      <span className="text-2xl mr-3">{badge.emoji}</span>
                      <div>
                        <h3 className="font-medium text-matrix-text">{concept.name}</h3>
                        {concept.subject && (
                          <p className="text-sm text-gray-400">{concept.subject}</p>
                        )}
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <div className={`text-lg font-bold ${getMasteryColor(concept.mastery)}`}>
                        {concept.mastery.toFixed(0)}%
                      </div>
                      <div className="text-xs text-gray-400">{badge.label}</div>
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="w-full bg-gray-700 rounded-full h-2 mb-3">
                    <div
                      className={`h-2 rounded-full transition-all duration-300 ${
                        concept.mastery >= 85 ? 'bg-green-400' :
                        concept.mastery >= 70 ? 'bg-yellow-400' : 'bg-red-400'
                      }`}
                      style={{ width: `${Math.min(concept.mastery, 100)}%` }}
                    ></div>
                  </div>

                  <div className="flex justify-between text-sm text-gray-400">
                    <span>{concept.attempts} attempt{concept.attempts !== 1 ? 's' : ''}</span>
                    {concept.last_reviewed && (
                      <span>
                        Last reviewed: {new Date(concept.last_reviewed).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* Learning Tips */}
      <div className="zen-card rounded-lg p-6">
        <h2 className="text-xl font-semibold text-matrix-text mb-4 flex items-center">
          <span className="mr-2">💡</span>
          Learning Tips
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div className="bg-gray-800 rounded p-4">
            <h3 className="font-medium text-matrix-accent mb-2">🎯 Mastery Goal</h3>
            <p className="text-gray-300">
              Aim for 85% or higher to achieve concept mastery. Review and retake quizzes to improve.
            </p>
          </div>
          <div className="bg-gray-800 rounded p-4">
            <h3 className="font-medium text-matrix-accent mb-2">🔄 Spaced Repetition</h3>
            <p className="text-gray-300">
              Review concepts regularly to strengthen long-term retention and understanding.
            </p>
          </div>
          <div className="bg-gray-800 rounded p-4">
            <h3 className="font-medium text-matrix-accent mb-2">🧠 Active Learning</h3>
            <p className="text-gray-300">
              Use the Feynman technique - explain concepts in your own words to deepen understanding.
            </p>
          </div>
          <div className="bg-gray-800 rounded p-4">
            <h3 className="font-medium text-matrix-accent mb-2">📈 Progressive Learning</h3>
            <p className="text-gray-300">
              Build on previous concepts and explore related topics to create strong knowledge connections.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProgressDashboard