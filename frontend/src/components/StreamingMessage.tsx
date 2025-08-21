import React from 'react'
import type { StreamingStep } from '../types'

interface StreamingMessageProps {
  steps: StreamingStep[]
}

const StreamingMessage: React.FC<StreamingMessageProps> = ({ steps }) => {
  const getStepIcon = (type: string, status: string) => {
    if (status === 'error') return '❌'
    if (status === 'completed') return '✅'
    
    // Active status icons
    switch (type) {
      case 'processing': return '🧠'
      case 'keywords': return '📝'
      case 'sources': return '🔍'
      case 'explanation': return '🤖'
      case 'visual': return '🎨'
      case 'finalizing': return '✨'
      case 'quiz': return '🎯'
      case 'grading': return '📊'
      case 'topics': return '🔗'
      default: return '⏳'
    }
  }

  const getStepAnimation = (status: string) => {
    switch (status) {
      case 'active':
        return 'animate-pulse'
      case 'completed':
        return 'animate-none'
      case 'error':
        return 'animate-bounce'
      default:
        return ''
    }
  }

  return (
    <div className="flex justify-start mb-4">
      <div className="max-w-3xl">
        <div className="flex items-start space-x-3">
          {/* AI Avatar */}
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-700 text-matrix-text flex items-center justify-center text-sm font-bold">
            🧠
          </div>
          
          {/* Streaming Steps */}
          <div className="flex-1">
            <div className="inline-block p-4 rounded-lg bg-gray-800 text-matrix-text">
              <div className="space-y-2">
                {steps.map((step, index) => (
                  <div 
                    key={step.id}
                    className={`
                      streaming-step flex items-center space-x-2 p-2 rounded
                      ${step.status === 'active' ? 'streaming-active thinking-glow' : ''}
                      ${getStepAnimation(step.status)} transition-all duration-300
                    `}
                  >
                    <span className="text-lg flex-shrink-0">{getStepIcon(step.type, step.status)}</span>
                    <div className="flex-1">
                      <div 
                        className={`text-sm ${
                          step.status === 'active' 
                            ? 'text-matrix-accent font-medium' 
                            : step.status === 'completed'
                              ? 'text-green-400'
                              : step.status === 'error'
                                ? 'text-red-400'
                                : 'text-gray-400'
                        }`}
                      >
                        {step.content}
                      </div>
                      {/* Brief description for active/completed steps */}
                      {(step.status === 'active' || step.status === 'completed') && step.brief && (
                        <div className="text-xs text-gray-500 mt-1 pl-2">
                          {step.brief}
                        </div>
                      )}
                    </div>
                    
                    {/* Loading dots for active steps */}
                    {step.status === 'active' && (
                      <div className="flex space-x-1 flex-shrink-0">
                        <div className="w-1.5 h-1.5 bg-matrix-accent rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                        <div className="w-1.5 h-1.5 bg-matrix-accent rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                        <div className="w-1.5 h-1.5 bg-matrix-accent rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                      </div>
                    )}
                    
                    {/* Completion checkmark animation */}
                    {step.status === 'completed' && (
                      <div className="flex-shrink-0">
                        <div className="w-4 h-4 bg-green-500 rounded-full flex items-center justify-center animate-ping">
                          <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
                
                {/* Progress bar */}
                <div className="mt-3 pt-2 border-t border-gray-700">
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 bg-gray-700 rounded-full h-1.5">
                      <div 
                        className="bg-matrix-accent h-1.5 rounded-full transition-all duration-500 ease-out"
                        style={{ 
                          width: `${(steps.filter(s => s.status === 'completed').length / Math.max(steps.length, 1)) * 100}%` 
                        }}
                      ></div>
                    </div>
                    <span className="text-xs text-gray-400">
                      {steps.filter(s => s.status === 'completed').length}/{steps.length}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Timestamp */}
            <div className="text-xs text-gray-500 mt-1 text-left">
              Processing...
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default StreamingMessage