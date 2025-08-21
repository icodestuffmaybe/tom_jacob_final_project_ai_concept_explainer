import React, { useState, useRef, useEffect } from 'react'
import ChatMessage from './components/ChatMessage'
import ChatInput from './components/ChatInput'
import type { Message } from './types'
import './App.css'

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'assistant',
      content: "Hello! I'm your AI concept explainer. I'll help you understand any topic using the Feynman technique with visual aids and interactive quizzes.\n\n**What concept would you like me to explain today?**",
      timestamp: new Date()
    }
  ])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const addMessage = (message: Omit<Message, 'id' | 'timestamp'>) => {
    const newMessage: Message = {
      ...message,
      id: Date.now().toString(),
      timestamp: new Date()
    }
    setMessages(prev => [...prev, newMessage])
  }

  const handleUserMessage = async (content: string) => {
    // Add user message
    addMessage({ type: 'user', content })
    setIsLoading(true)

    try {
      // Determine the type of user response
      const lastAssistantMessage = messages.filter(m => m.type === 'assistant').slice(-1)[0]
      const isQuizResponse = lastAssistantMessage?.metadata?.expectingQuizAnswer
      const isTopicSelection = lastAssistantMessage?.metadata?.expectingTopicSelection
      const isQuizAnswer = lastAssistantMessage?.metadata?.expectingQuizAnswers

      if (isQuizAnswer) {
        // Handle quiz answer submission
        await handleQuizSubmission(content, lastAssistantMessage.metadata.quizId)
      } else if (isQuizResponse) {
        // Handle yes/no quiz response
        await handleQuizResponse(content.toLowerCase())
      } else if (isTopicSelection) {
        // Handle topic selection
        await handleTopicSelection(content, lastAssistantMessage.metadata.topics)
      } else {
        // Handle new concept explanation request
        await handleConceptExplanation(content)
      }
    } catch (error) {
      addMessage({
        type: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        isError: true
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleConceptExplanation = async (query: string) => {
    // Add thinking message
    addMessage({
      type: 'assistant',
      content: '🧠 Let me explain that for you... This will take a moment while I:\n- Research the topic\n- Create a visual explanation\n- Prepare it using the Feynman technique',
      isThinking: true
    })

    try {
      const response = await fetch('http://localhost:8000/api/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })

      const data = await response.json()

      // Add explanation with SVG
      addMessage({
        type: 'assistant',
        content: data.explanation,
        svgContent: data.svg_flashcard,
        sources: data.sources,
        keywords: data.keywords
      })

      // Ask about quiz
      addMessage({
        type: 'assistant',
        content: '**Great! Now that you\'ve learned about this concept...**\n\nWould you like to test your understanding with a quick 5-question quiz? 🧩\n\nJust say "yes" or "no"!',
        metadata: { 
          expectingQuizAnswer: true, 
          sessionId: data.session_id,
          lastTopic: query
        }
      })

    } catch (error) {
      addMessage({
        type: 'assistant',
        content: 'Sorry, I had trouble generating the explanation. Please try again.',
        isError: true
      })
    }
  }

  const handleQuizResponse = async (response: string) => {
    const lastMessage = messages.filter(m => m.type === 'assistant').slice(-1)[0]
    const sessionId = lastMessage?.metadata?.sessionId
    const lastTopic = lastMessage?.metadata?.lastTopic

    if (response.includes('yes') || response.includes('y')) {
      // Generate quiz
      addMessage({
        type: 'assistant',
        content: '🎯 Excellent! Let me create a quiz for you...',
        isThinking: true
      })

      try {
        const quizResponse = await fetch('http://localhost:8000/api/quiz/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session_id: sessionId, difficulty: 'medium' })
        })

        const quizData = await quizResponse.json()
        
        let quizContent = '**📝 Quiz Time!**\n\nAnswer these 5 questions (just type the letter: A, B, C, or D):\n\n'
        
        quizData.questions.forEach((q: any, index: number) => {
          quizContent += `**${index + 1}. ${q.question}**\n`
          if (q.options) {
            q.options.forEach((option: string, optIndex: number) => {
              const letter = String.fromCharCode(65 + optIndex) // A, B, C, D
              quizContent += `${letter}) ${option}\n`
            })
          }
          quizContent += '\n'
        })

        quizContent += 'Please type your answers like: A, B, C, D, A'

        addMessage({
          type: 'assistant',
          content: quizContent,
          metadata: { 
            expectingQuizAnswers: true, 
            quizId: quizData.quiz_id,
            questions: quizData.questions
          }
        })

      } catch (error) {
        addMessage({
          type: 'assistant',
          content: 'Sorry, I had trouble creating the quiz. Let me suggest some related topics instead.',
          isError: true
        })
        await suggestRelatedTopics(lastTopic)
      }

    } else {
      // Suggest related topics
      await suggestRelatedTopics(lastTopic)
    }
  }

  const handleQuizSubmission = async (answers: string, quizId: string) => {
    const lastMessage = messages.filter(m => m.type === 'assistant').slice(-1)[0]
    const questions = lastMessage?.metadata?.questions || []

    // Parse answers (A, B, C, D, A format)
    const answerArray = answers.split(',').map(a => a.trim().toUpperCase())
    
    if (answerArray.length !== questions.length) {
      addMessage({
        type: 'assistant',
        content: `Please provide exactly ${questions.length} answers in the format: A, B, C, D, A`,
        isError: true
      })
      return
    }

    addMessage({
      type: 'assistant',
      content: '📊 Checking your answers...',
      isThinking: true
    })

    try {
      // Convert letter answers to actual option text
      const formattedAnswers = answerArray.map((letter, index) => {
        const question = questions[index]
        const optionIndex = letter.charCodeAt(0) - 65 // A=0, B=1, etc.
        const answer = question.options?.[optionIndex] || letter
        
        return {
          question_id: question.id,
          answer: answer
        }
      })

      const response = await fetch('http://localhost:8000/api/quiz/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          quiz_id: quizId, 
          answers: formattedAnswers 
        })
      })

      const result = await response.json()
      
      let resultContent = `**🎉 Quiz Results**\n\n`
      resultContent += `**Score: ${result.score.toFixed(0)}%** (${result.correct_answers}/${result.total_questions} correct)\n\n`
      
      if (result.mastery_achieved) {
        resultContent += '🏆 **Excellent! You\'ve mastered this concept!**\n\n'
      } else if (result.score >= 70) {
        resultContent += '👏 **Good work! You\'re getting there.**\n\n'
      } else {
        resultContent += '📚 **Keep studying - you\'ll get it next time!**\n\n'
      }

      // Add detailed feedback
      result.feedback.forEach((feedback: any, index: number) => {
        const letter = String.fromCharCode(65 + index)
        resultContent += `**${index + 1}.** ${feedback.correct ? '✅' : '❌'} `
        if (feedback.correct_answer) {
          resultContent += `Correct answer: ${feedback.correct_answer}\n`
        }
        resultContent += `${feedback.explanation}\n\n`
      })

      addMessage({
        type: 'assistant',
        content: resultContent
      })

      // Suggest related topics after quiz
      const lastTopic = lastMessage?.metadata?.lastTopic
      await suggestRelatedTopics(lastTopic)

    } catch (error) {
      addMessage({
        type: 'assistant',
        content: 'Sorry, I had trouble grading the quiz. Please try again.',
        isError: true
      })
    }
  }

  const suggestRelatedTopics = async (lastTopic: string) => {
    // Generate related topics (simplified version)
    const relatedTopics = generateRelatedTopics(lastTopic)
    
    let topicContent = '**🔗 Related Topics You Might Find Interesting:**\n\n'
    relatedTopics.forEach((topic, index) => {
      topicContent += `${index + 1}. ${topic}\n`
    })
    topicContent += '\n**Just type the number (1-5) of any topic you\'d like me to explain, or ask about something completely different!**'

    addMessage({
      type: 'assistant',
      content: topicContent,
      metadata: { 
        expectingTopicSelection: true, 
        topics: relatedTopics,
        lastTopic 
      }
    })
  }

  const handleTopicSelection = async (input: string, topics: string[]) => {
    const selection = parseInt(input.trim())
    
    if (selection >= 1 && selection <= topics.length) {
      const selectedTopic = topics[selection - 1]
      addMessage({
        type: 'user',
        content: selectedTopic
      })
      await handleConceptExplanation(selectedTopic)
    } else {
      // Treat as new concept request
      await handleConceptExplanation(input)
    }
  }

  const generateRelatedTopics = (topic: string): string[] => {
    // Simple topic generation - in a real app, this could be more sophisticated
    const topicLower = topic.toLowerCase()
    
    if (topicLower.includes('photosynthesis')) {
      return [
        'Cellular respiration',
        'Chloroplasts and cell structure',
        'The carbon cycle',
        'Plant nutrition and growth',
        'Ecosystems and food chains'
      ]
    } else if (topicLower.includes('math') || topicLower.includes('theorem')) {
      return [
        'Basic algebra concepts',
        'Geometry fundamentals',
        'Mathematical proofs',
        'Real-world math applications',
        'History of mathematics'
      ]
    } else {
      // Generic related topics
      return [
        `History of ${topic}`,
        `${topic} in modern society`,
        `How ${topic} works`,
        `Applications of ${topic}`,
        `Future of ${topic}`
      ]
    }
  }

  return (
    <div className="min-h-screen bg-matrix-bg text-matrix-text flex flex-col">
      {/* Header */}
      <nav className="border-b border-gray-700 p-4 flex-shrink-0">
        <div className="container mx-auto">
          <h1 className="text-xl font-bold matrix-text">🧠 AI Concept Explainer</h1>
          <p className="text-sm text-gray-400">Learning made simple with AI</p>
        </div>
      </nav>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-800 rounded-lg p-4 max-w-xs">
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-matrix-accent"></div>
                  <span className="text-sm text-gray-400">AI is thinking...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Chat Input */}
      <div className="border-t border-gray-700 p-4 flex-shrink-0">
        <div className="max-w-4xl mx-auto">
          <ChatInput 
            onSendMessage={handleUserMessage} 
            disabled={isLoading}
            placeholder="Type your concept or answer here..."
          />
        </div>
      </div>
    </div>
  )
}

export default App