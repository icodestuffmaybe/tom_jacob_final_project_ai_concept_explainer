import React, { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import SVGFlashcard from './SVGFlashcard'
import SourcePanel from './SourcePanel'
import QuizInterface_simple from './QuizInterface_simple'
import type { Explanation } from '../types'

interface ExplanationDisplayProps {
  explanation: Explanation
}

const ExplanationDisplay: React.FC<ExplanationDisplayProps> = ({ explanation }) => {
  const [activeTab, setActiveTab] = useState<'explanation' | 'visual' | 'quiz'>('explanation')
  const [showSources, setShowSources] = useState(false)

  const tabs = [
    { id: 'explanation', label: 'Explanation', icon: '📚' },
    { id: 'visual', label: 'Visual', icon: '🎨' },
    { id: 'quiz', label: 'Quiz', icon: '❓' },
  ] as const

  return (
    <div className="zen-card rounded-lg overflow-hidden">
      {/* Tab Navigation */}
      <div className="flex border-b border-gray-600">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 py-3 px-4 text-center font-medium transition-colors ${
              activeTab === tab.id
                ? 'bg-matrix-accent text-black'
                : 'bg-gray-800 text-matrix-text hover:bg-gray-700'
            }`}
          >
            <span className="mr-2">{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="p-6">
        {activeTab === 'explanation' && (
          <div className="space-y-4">
            <div className="prose prose-invert max-w-none">
              <ReactMarkdown className="text-matrix-text leading-relaxed">
                {explanation.explanation}
              </ReactMarkdown>
            </div>

            {explanation.keywords && explanation.keywords.length > 0 && (
              <div className="mt-4">
                <h4 className="text-sm font-semibold text-gray-400 mb-2">
                  Key Concepts:
                </h4>
                <div className="flex flex-wrap gap-2">
                  {explanation.keywords.map((keyword, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-gray-700 text-matrix-accent text-sm rounded"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {explanation.sources && explanation.sources.length > 0 && (
              <div className="mt-6">
                <button
                  onClick={() => setShowSources(!showSources)}
                  className="flex items-center text-matrix-accent hover:text-green-400 text-sm"
                >
                  <span className="mr-2">📖</span>
                  {showSources ? 'Hide' : 'Show'} Sources ({explanation.sources.length})
                </button>
                
                {showSources && (
                  <div className="mt-3">
                    <SourcePanel sources={explanation.sources} />
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {activeTab === 'visual' && (
          <div className="flex justify-center">
            <SVGFlashcard svgContent={explanation.svg_flashcard} />
          </div>
        )}

        {activeTab === 'quiz' && (
          <QuizInterface_simple sessionId={explanation.session_id} />
        )}
      </div>
    </div>
  )
}

export default ExplanationDisplay