import React from 'react'
import type { Source } from '../types'

interface SourcePanelProps {
  sources: Source[]
}

const SourcePanel: React.FC<SourcePanelProps> = ({ sources }) => {
  if (!sources || sources.length === 0) {
    return (
      <div className="text-center text-gray-400 py-4">
        <p>No sources available</p>
      </div>
    )
  }

  const getSourceIcon = (sourceType: string) => {
    switch (sourceType) {
      case 'wikipedia':
        return '📰'
      case 'duckduckgo_educational':
        return '🦆'
      case 'web':
        return '🌐'
      default:
        return '📄'
    }
  }

  const getSourceLabel = (sourceType: string) => {
    switch (sourceType) {
      case 'wikipedia':
        return 'Wikipedia'
      case 'duckduckgo_educational':
        return 'Educational Web'
      case 'web':
        return 'Web'
      default:
        return sourceType
    }
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-matrix-text flex items-center">
        <span className="mr-2">🔍</span>
        Verified Sources
      </h3>
      
      <div className="space-y-3">
        {sources.map((source, index) => (
          <div
            key={index}
            className="bg-gray-800 rounded-lg p-4 border border-gray-600 hover:border-matrix-accent transition-colors"
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center">
                <span className="mr-2 text-lg">{getSourceIcon(source.source_type)}</span>
                <h4 className="font-medium text-matrix-text">
                  [{index + 1}] {source.title}
                </h4>
              </div>
              <span className="text-xs text-gray-400 bg-gray-700 px-2 py-1 rounded">
                {getSourceLabel(source.source_type)}
              </span>
            </div>
            
            <p className="text-gray-300 text-sm mb-3 leading-relaxed">
              {source.snippet}
            </p>
            
            {source.url && (
              <a
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center text-matrix-accent hover:text-green-400 text-sm"
              >
                <span className="mr-1">🔗</span>
                Read full article
                <span className="ml-1">↗</span>
              </a>
            )}
          </div>
        ))}
      </div>
      
      <div className="text-xs text-gray-400 text-center pt-2 border-t border-gray-600">
        Sources are automatically verified for credibility and educational value
      </div>
    </div>
  )
}

export default SourcePanel