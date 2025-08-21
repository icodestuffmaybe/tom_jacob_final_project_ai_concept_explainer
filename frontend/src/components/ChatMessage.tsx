import React from 'react'
import ReactMarkdown from 'react-markdown'
import QuizInterface from './QuizInterface_radio'
import type { Message } from '../types'

interface ChatMessageProps {
  message: Message
  onQuizSubmit?: (answers: Record<string, string>) => void
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, onQuizSubmit }) => {
  const isUser = message.type === 'user'
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-3xl ${isUser ? 'order-2' : 'order-1'}`}>
        
        {/* Avatar */}
        <div className={`flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
          <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
            isUser 
              ? 'bg-matrix-accent text-black' 
              : 'bg-gray-700 text-matrix-text'
          }`}>
            {isUser ? '👤' : '🧠'}
          </div>
          
          {/* Message Content */}
          <div className={`flex-1 ${isUser ? 'text-right' : 'text-left'}`}>
            <div className={`inline-block p-4 rounded-lg ${
              isUser 
                ? 'bg-matrix-accent text-black' 
                : message.isError 
                  ? 'bg-red-900/30 border border-red-600 text-matrix-text'
                  : message.isThinking
                    ? 'bg-blue-900/30 border border-blue-600 text-matrix-text'
                    : 'bg-gray-800 text-matrix-text'
            }`}>
              
              {/* Main content */}
              <div className="prose prose-invert max-w-none">
                <ReactMarkdown 
                  className={`${isUser ? 'text-black' : 'text-matrix-text'} leading-relaxed`}
                  components={{
                    // Custom styling for markdown elements
                    strong: ({children}) => (
                      <strong className={isUser ? 'text-black' : 'text-matrix-accent'}>{children}</strong>
                    ),
                    h1: ({children}) => (
                      <h1 className={`text-xl font-bold mb-2 ${isUser ? 'text-black' : 'text-matrix-accent'}`}>{children}</h1>
                    ),
                    h2: ({children}) => (
                      <h2 className={`text-lg font-bold mb-2 ${isUser ? 'text-black' : 'text-matrix-accent'}`}>{children}</h2>
                    ),
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              </div>

              {/* SVG Flashcard */}
              {message.svgContent && !isUser && (
                <div className="mt-4 p-4 bg-gray-900 rounded-lg">
                  <h4 className="text-sm font-semibold text-matrix-accent mb-2">
                    📊 Visual Learning Aid
                  </h4>
                  <div 
                    className="rounded-lg overflow-hidden"
                    dangerouslySetInnerHTML={{ __html: message.svgContent }}
                  />
                </div>
              )}

              {/* Quiz Interface */}
              {message.isQuiz && message.quizData && !isUser && onQuizSubmit && (
                <div className="mt-4">
                  <QuizInterface
                    questions={message.quizData.questions}
                    onSubmit={(answers) => onQuizSubmit(answers)}
                    isLoading={false}
                  />
                </div>
              )}

              {/* Keywords */}
              {message.keywords && message.keywords.length > 0 && !isUser && (
                <div className="mt-3">
                  <h4 className="text-xs font-semibold text-gray-400 mb-1">
                    🏷️ Key Concepts:
                  </h4>
                  <div className="flex flex-wrap gap-1">
                    {message.keywords.map((keyword, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-gray-700 text-matrix-accent text-xs rounded"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Sources */}
              {message.sources && message.sources.length > 0 && !isUser && (
                <div className="mt-3">
                  <details className="cursor-pointer">
                    <summary className="text-xs font-semibold text-gray-400 hover:text-matrix-accent">
                      📚 Sources ({message.sources.length}) - Click to expand
                    </summary>
                    <div className="mt-2 space-y-2">
                      {message.sources.map((source, index) => (
                        <div key={index} className="bg-gray-900 rounded p-2">
                          <div className="flex items-center mb-1">
                            <span className="text-xs text-matrix-accent mr-2">[{index + 1}]</span>
                            <h5 className="text-xs font-medium text-matrix-text">{source.title}</h5>
                          </div>
                          <p className="text-xs text-gray-400 mb-1">{source.snippet}</p>
                          {source.url && (
                            <a
                              href={source.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-xs text-matrix-accent hover:text-green-400"
                            >
                              🔗 Read more ↗
                            </a>
                          )}
                        </div>
                      ))}
                    </div>
                  </details>
                </div>
              )}
            </div>
            
            {/* Timestamp */}
            <div className={`text-xs text-gray-500 mt-1 ${isUser ? 'text-right' : 'text-left'}`}>
              {message.timestamp.toLocaleTimeString()}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChatMessage