import React, { useState, useRef, useEffect } from 'react'
import ChatMessage from './components/ChatMessage'
import ChatInput from './components/ChatInput'
import StreamingMessage from './components/StreamingMessage'
import type { Message, StreamingStep } from './types'
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
  const [streamingSteps, setStreamingSteps] = useState<StreamingStep[]>([])
  const [currentStreamingId, setCurrentStreamingId] = useState<string | null>(null)
  const [isStreamingCollapsed, setIsStreamingCollapsed] = useState(false)
  const [streamingCompleted, setStreamingCompleted] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, streamingSteps])

  const addMessage = (message: Omit<Message, 'id' | 'timestamp'>) => {
    const newMessage: Message = {
      ...message,
      id: Date.now().toString(),
      timestamp: new Date()
    }
    setMessages(prev => [...prev, newMessage])
    return newMessage.id
  }

  const addStreamingStep = (step: Omit<StreamingStep, 'id' | 'timestamp'>) => {
    const newStep: StreamingStep = {
      ...step,
      id: Date.now().toString(),
      timestamp: new Date()
    }
    setStreamingSteps(prev => [...prev, newStep])
  }

  const clearStreaming = () => {
    // Mark streaming as completed and collapse it
    setStreamingCompleted(true)
    setIsStreamingCollapsed(true)
    setCurrentStreamingId(null)
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
        await handleQuizSubmission(content, lastAssistantMessage.metadata.quizId)
      } else if (isQuizResponse) {
        await handleQuizResponse(content.toLowerCase())
      } else if (isTopicSelection) {
        await handleTopicSelection(content, lastAssistantMessage.metadata.topics)
      } else {
        await handleConceptExplanation(content)
      }
    } catch (error) {
      clearStreaming()
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
    // Reset streaming state for new explanation
    setStreamingSteps([])
    setStreamingCompleted(false)
    setIsStreamingCollapsed(false)
    
    // Start streaming process
    const streamingId = Date.now().toString()
    setCurrentStreamingId(streamingId)
    
    // Step 1: Start processing
    addStreamingStep({
      type: 'processing',
      content: 'Processing your request...',
      brief: 'Analyzing your query and preparing to search for information',
      status: 'active'
    })

    await sleep(500)

    // Step 2: Extracting keywords
    addStreamingStep({
      type: 'keywords',
      content: 'Extracting key concepts and search terms...',
      brief: 'Identifying the most important keywords and related concepts to search for',
      status: 'active'
    })

    await sleep(800)

    // Step 3: Searching sources
    addStreamingStep({
      type: 'sources',
      content: 'Searching Wikipedia and educational sources...',
      brief: 'Looking through Wikipedia and educational websites for reliable information',
      status: 'active'
    })

    await sleep(1000)

    try {
      // Make the actual API call
      const response = await fetch('http://localhost:8000/api/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })

      const data = await response.json()

      // Step 4: Found sources
      addStreamingStep({
        type: 'sources',
        content: `Found ${data.sources?.length || 0} credible sources`,
        brief: `Successfully located authoritative sources including ${data.sources?.map(s => s.source_type).join(', ') || 'educational content'}`,
        status: 'completed'
      })

      await sleep(500)

      // Step 5: Generating explanation
      addStreamingStep({
        type: 'explanation',
        content: 'Generating explanation using Feynman technique...',
        brief: 'Creating a simple, clear explanation that breaks down complex concepts into easy-to-understand language',
        status: 'active'
      })

      await sleep(1200)

      // Step 6: Creating visual
      addStreamingStep({
        type: 'visual',
        content: 'Creating AI-generated visual flashcard...',
        brief: 'Designing a visual diagram or illustration to help you understand the concept better',
        status: 'active'
      })

      await sleep(1000)

      // Step 7: Finalizing
      addStreamingStep({
        type: 'finalizing',
        content: 'Finalizing your personalized explanation...',
        brief: 'Putting together the explanation, visual, and sources into a complete learning experience',
        status: 'active'
      })

      await sleep(500)

      // Clear streaming and add final result
      clearStreaming()

      // Add the complete explanation
      addMessage({
        type: 'assistant',
        content: data.explanation,
        svgContent: data.svg_flashcard,
        sources: data.sources,
        keywords: data.keywords
      })

      await sleep(800)

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
      // Update last step to show error
      setStreamingSteps(prev => 
        prev.map((step, index) => 
          index === prev.length - 1 
            ? { ...step, status: 'error', content: '❌ ' + step.content.replace('🎨', '').replace('🤖', '').replace('✨', '') + ' - Error occurred' }
            : step
        )
      )
      
      await sleep(1000)
      clearStreaming()
      
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
      // Start streaming for quiz generation
      const streamingId = Date.now().toString()
      setCurrentStreamingId(streamingId)
      
      addStreamingStep({
        type: 'quiz',
        content: 'Creating personalized quiz questions...',
        brief: 'Generating questions that test your understanding of the key concepts you just learned',
        status: 'active'
      })

      await sleep(800)

      addStreamingStep({
        type: 'quiz',
        content: 'Adjusting difficulty level...',
        brief: 'Setting appropriate difficulty based on the complexity of the topic',
        status: 'active'
      })

      await sleep(600)

      try {
        const quizResponse = await fetch('http://localhost:8000/api/quiz/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session_id: sessionId, difficulty: 'medium' })
        })

        const quizData = await quizResponse.json()
        
        addStreamingStep({
          type: 'quiz',
          content: 'Generated 5 multiple-choice questions',
          brief: 'Quiz questions are ready to test your knowledge on this topic',
          status: 'completed'
        })

        await sleep(500)
        clearStreaming()
        
        // Add quiz with interactive interface
        addMessage({
          type: 'assistant',
          content: '**📝 Quiz Time!**\n\nPlease answer all 5 questions by selecting the best option:',
          isQuiz: true,
          quizData: {
            quizId: quizData.quiz_id,
            questions: quizData.questions
          },
          metadata: { 
            expectingQuizAnswers: true, 
            quizId: quizData.quiz_id,
            questions: quizData.questions
          }
        })

      } catch (error) {
        clearStreaming()
        addMessage({
          type: 'assistant',
          content: 'Sorry, I had trouble creating the quiz. Let me suggest some related topics instead.',
          isError: true
        })
        await suggestRelatedTopics(lastTopic)
      }

    } else {
      await suggestRelatedTopics(lastTopic)
    }
  }

  const handleQuizSubmitFromInterface = async (selectedAnswers: Record<string, string>) => {
    // Find the quiz message to get the quiz ID
    const quizMessage = messages.filter(m => m.isQuiz).slice(-1)[0]
    if (!quizMessage?.quizData) return

    const quizId = quizMessage.quizData.quizId
    const questions = quizMessage.quizData.questions

    // Convert selected answers to the expected format
    const formattedAnswers = questions.map(question => ({
      question_id: question.id,
      answer: selectedAnswers[question.id] || ''
    }))

    await handleQuizSubmissionInternal(formattedAnswers, quizId)
  }

  const handleQuizSubmission = async (answers: string, quizId: string) => {
    const lastMessage = messages.filter(m => m.type === 'assistant').slice(-1)[0]
    const questions = lastMessage?.metadata?.questions || []

    const answerArray = answers.split(',').map(a => a.trim().toUpperCase())
    
    if (answerArray.length !== questions.length) {
      addMessage({
        type: 'assistant',
        content: `Please provide exactly ${questions.length} answers in the format: A, B, C, D, A`,
        isError: true
      })
      return
    }

    // Start streaming for quiz evaluation
    const streamingId = Date.now().toString()
    setCurrentStreamingId(streamingId)
    
    addStreamingStep({
      type: 'grading',
      content: 'Evaluating your answers...',
      brief: 'Checking each answer against the correct solutions',
      status: 'active'
    })

    await sleep(600)

    addStreamingStep({
      type: 'grading',
      content: 'Calculating your score...',
      brief: 'Computing your overall performance and identifying areas for improvement',
      status: 'active'
    })

    await sleep(500)

    addStreamingStep({
      type: 'grading',
      content: 'Preparing detailed feedback...',
      brief: 'Creating personalized explanations for each question to help you learn',
      status: 'active'
    })

    try {
      const formattedAnswers = answerArray.map((letter, index) => {
        const question = questions[index]
        const optionIndex = letter.charCodeAt(0) - 65
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
      
      addStreamingStep({
        type: 'grading',
        content: `Quiz completed! Score: ${result.score.toFixed(0)}%`,
        brief: `Your learning assessment is complete with detailed feedback for each question`,
        status: 'completed'
      })

      await sleep(800)
      clearStreaming()
      
      let resultContent = `**🎉 Quiz Results**\n\n`
      resultContent += `**Score: ${result.score.toFixed(0)}%** (${result.correct_answers}/${result.total_questions} correct)\n\n`
      
      // Analyze specific mistakes for targeted feedback
      const incorrectAnswers = result.feedback.filter(f => !f.correct)
      const conceptGaps = []
      
      // Extract key concepts from wrong answers
      incorrectAnswers.forEach(feedback => {
        if (feedback.explanation) {
          const explanation = feedback.explanation.toLowerCase()
          if (explanation.includes('definition') || explanation.includes('meaning') || explanation.includes('term')) {
            conceptGaps.push('basic definitions')
          }
          if (explanation.includes('process') || explanation.includes('mechanism') || explanation.includes('how') || explanation.includes('steps')) {
            conceptGaps.push('understanding processes')
          }
          if (explanation.includes('application') || explanation.includes('example') || explanation.includes('use') || explanation.includes('real-world')) {
            conceptGaps.push('practical applications')
          }
          if (explanation.includes('relationship') || explanation.includes('connection') || explanation.includes('between') || explanation.includes('related')) {
            conceptGaps.push('concept relationships')
          }
          if (explanation.includes('formula') || explanation.includes('calculation') || explanation.includes('equation') || explanation.includes('mathematical')) {
            conceptGaps.push('mathematical concepts')
          }
        }
      })
      
      // Performance feedback
      if (result.mastery_achieved) {
        resultContent += '🏆 **Excellent! You\'ve mastered this concept!**\n\n'
      } else if (result.score >= 70) {
        resultContent += '👏 **Good work! You\'re getting there.**\n\n'
      } else {
        resultContent += '📚 **Keep studying - you\'ll get it next time!**\n\n'
      }

      // Detailed feedback
      result.feedback.forEach((feedback: any, index: number) => {
        resultContent += `**${index + 1}.** ${feedback.correct ? '✅' : '❌'} `
        if (feedback.correct_answer) {
          resultContent += `Correct answer: ${feedback.correct_answer}\n`
        }
        resultContent += `${feedback.explanation}\n\n`
      })
      
      // Generate specific recap and advice
      let recap = ''
      let advice = ''
      
      if (result.mastery_achieved) {
        recap = 'Outstanding performance! You demonstrated strong understanding across all key areas.'
        advice = 'Consider exploring advanced applications or teaching this concept to someone else to reinforce your mastery.'
      } else if (result.score >= 70) {
        recap = `Good progress! You got ${result.correct_answers} out of ${result.total_questions} questions correct.`
        if (conceptGaps.length > 0) {
          recap += ` Your main challenges were in ${[...new Set(conceptGaps)].slice(0, 2).join(' and ')}.`
        }
        advice = 'Focus on the areas you missed. '
        if (conceptGaps.includes('basic definitions')) {
          advice += 'Review key definitions and terminology. '
        }
        if (conceptGaps.includes('understanding processes')) {
          advice += 'Study the step-by-step processes and mechanisms. '
        }
        if (conceptGaps.includes('practical applications')) {
          advice += 'Look for real-world examples and applications. '
        }
        if (conceptGaps.includes('concept relationships')) {
          advice += 'Focus on how different concepts connect to each other. '
        }
        if (conceptGaps.includes('mathematical concepts')) {
          advice += 'Practice the mathematical relationships and formulas. '
        }
        if (advice === 'Focus on the areas you missed. ') {
          advice = 'Review the specific questions you missed and try to understand the reasoning behind each correct answer.'
        }
      } else {
        recap = `You're building your foundation! You got ${result.correct_answers} out of ${result.total_questions} questions correct.`
        if (conceptGaps.length > 0) {
          recap += ` The main areas to work on are ${[...new Set(conceptGaps)].slice(0, 3).join(', ')}.`
        }
        advice = 'Start with the fundamentals. '
        if (conceptGaps.includes('basic definitions')) {
          advice += 'Make sure you understand the core definitions first. '
        }
        if (conceptGaps.includes('understanding processes')) {
          advice += 'Break down complex processes into simple steps. '
        }
        advice += 'Use visual aids, create your own examples, and practice explaining concepts in simple terms.'
      }
      
      // Add recap and learning advice
      resultContent += `---\n\n**📈 Learning Recap:**\n${recap}\n\n`
      resultContent += `**🎯 Personalized Next Steps:**\n${advice}\n\n`
      
      // Specific study tips based on identified gaps
      if (result.score < 70) {
        resultContent += `**📝 Targeted Study Tips:**\n`
        if (conceptGaps.includes('basic definitions')) {
          resultContent += `• Create flashcards for key terms and definitions\n`
        }
        if (conceptGaps.includes('understanding processes')) {
          resultContent += `• Draw flowcharts or diagrams showing step-by-step processes\n`
        }
        if (conceptGaps.includes('practical applications')) {
          resultContent += `• Find real-world examples and case studies\n`
        }
        if (conceptGaps.includes('concept relationships')) {
          resultContent += `• Create concept maps showing how ideas connect\n`
        }
        if (conceptGaps.includes('mathematical concepts')) {
          resultContent += `• Practice calculations and work through example problems\n`
        }
        if (conceptGaps.length === 0) {
          resultContent += `• Review the explanations for questions you missed\n`
          resultContent += `• Try explaining concepts in your own words\n`
          resultContent += `• Look for patterns in your incorrect answers\n`
        }
        resultContent += `\n`
      } else {
        resultContent += `**🚀 Continue Building Mastery:**\n`
        if (conceptGaps.length > 0) {
          resultContent += `• Strengthen your understanding of ${[...new Set(conceptGaps)].slice(0, 2).join(' and ')}\n`
        }
        resultContent += `• Explore advanced applications of this concept\n`
        resultContent += `• Try teaching this concept to someone else\n`
        resultContent += `• Look for connections to related topics\n\n`
      }

      addMessage({
        type: 'assistant',
        content: resultContent
      })

      const lastTopic = lastMessage?.metadata?.lastTopic
      if (lastTopic) {
        await suggestRelatedTopics(lastTopic)
      }

    } catch (error) {
      clearStreaming()
      addMessage({
        type: 'assistant',
        content: 'Sorry, I had trouble grading the quiz. Please try again.',
        isError: true
      })
    }
  }

  const suggestRelatedTopics = async (lastTopic: string) => {
    // Add small delay and streaming for topic generation
    const streamingId = Date.now().toString()
    setCurrentStreamingId(streamingId)
    
    addStreamingStep({
      type: 'topics',
      content: 'Finding related topics you might enjoy...',
      brief: 'Analyzing the topic to discover relevant concepts that build on what you just learned',
      status: 'active'
    })

    await sleep(800)

    const relatedTopics = generateRelatedTopics(lastTopic)
    
    addStreamingStep({
      type: 'topics',
      content: `Found ${relatedTopics.length} contextually relevant topics`,
      brief: 'Selected topics that naturally connect to and extend your current understanding',
      status: 'completed'
    })

    await sleep(500)
    clearStreaming()
    
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
    const inputTrimmed = input.trim()
    const selection = parseInt(inputTrimmed)
    
    // Check if user entered a valid number
    if (selection >= 1 && selection <= topics.length) {
      const selectedTopic = topics[selection - 1]
      await handleConceptExplanation(selectedTopic)
    } 
    // Check if user typed something similar to one of the topics
    else {
      const inputLower = inputTrimmed.toLowerCase()
      const matchedTopic = topics.find(topic => 
        topic.toLowerCase().includes(inputLower) || 
        inputLower.includes(topic.toLowerCase().split(' ')[0]) // Match first word
      )
      
      if (matchedTopic) {
        await handleConceptExplanation(matchedTopic)
      } else {
        // Treat as a new topic
        await handleConceptExplanation(inputTrimmed)
      }
    }
  }

  const generateRelatedTopics = (topic: string): string[] => {
    const topicLower = topic.toLowerCase()
    
    // Science topics
    if (topicLower.includes('photosynthesis')) {
      return [
        'Cellular respiration',
        'Chloroplasts and cell structure',
        'The carbon cycle',
        'Plant nutrition and growth',
        'Ecosystems and food chains'
      ]
    } else if (topicLower.includes('water') && (topicLower.includes('state') || topicLower.includes('phase'))) {
      return [
        'Phase transitions and energy',
        'Molecular behavior in different states',
        'Sublimation and deposition',
        'Critical point and triple point',
        'States of matter in everyday life'
      ]
    } else if (topicLower.includes('gravity') || topicLower.includes('gravitational')) {
      return [
        'Newton\'s laws of motion',
        'Orbital mechanics',
        'Tides and lunar effects',
        'Weight vs mass',
        'Einstein\'s general relativity'
      ]
    } else if (topicLower.includes('atom') || topicLower.includes('atomic')) {
      return [
        'Electron configuration',
        'Chemical bonding',
        'Periodic table trends',
        'Isotopes and radioactivity',
        'Quantum mechanics basics'
      ]
    } else if (topicLower.includes('dna') || topicLower.includes('genetic')) {
      return [
        'RNA and protein synthesis',
        'Gene expression and regulation',
        'Heredity and inheritance',
        'Mutations and evolution',
        'CRISPR and genetic engineering'
      ]
    } else if (topicLower.includes('evolution') || topicLower.includes('natural selection')) {
      return [
        'Genetics and heredity',
        'Fossil evidence',
        'Speciation and biodiversity',
        'Adaptation and survival',
        'Human evolution'
      ]
    }
    
    // Technology and AI topics
    else if (topicLower.includes('machine learning') || topicLower.includes('ai') || topicLower.includes('artificial intelligence')) {
      return [
        'Neural networks basics',
        'Deep learning fundamentals',
        'Supervised vs unsupervised learning',
        'AI ethics and bias',
        'Computer vision and NLP'
      ]
    } else if (topicLower.includes('neural network') || topicLower.includes('deep learning')) {
      return [
        'Backpropagation algorithm',
        'Convolutional neural networks',
        'Recurrent neural networks',
        'Gradient descent optimization',
        'Overfitting and regularization'
      ]
    } else if (topicLower.includes('embedding') || topicLower.includes('vector')) {
      return [
        'Natural language processing',
        'Similarity and distance metrics',
        'Dimensionality reduction',
        'Word2Vec and GloVe',
        'Transformer models'
      ]
    } else if (topicLower.includes('algorithm') || topicLower.includes('programming')) {
      return [
        'Data structures fundamentals',
        'Big O notation and complexity',
        'Sorting and searching algorithms',
        'Graph algorithms',
        'Dynamic programming'
      ]
    } else if (topicLower.includes('data structure')) {
      return [
        'Arrays and linked lists',
        'Trees and binary search trees',
        'Hash tables and dictionaries',
        'Stacks and queues',
        'Graphs and networks'
      ]
    }
    
    // Mathematics topics
    else if (topicLower.includes('calculus') || topicLower.includes('derivative') || topicLower.includes('integral')) {
      return [
        'Limits and continuity',
        'Applications of derivatives',
        'Integration techniques',
        'Differential equations',
        'Vector calculus'
      ]
    } else if (topicLower.includes('algebra') || topicLower.includes('equation')) {
      return [
        'Linear equations and systems',
        'Quadratic functions',
        'Exponential and logarithmic functions',
        'Polynomial operations',
        'Matrix algebra'
      ]
    } else if (topicLower.includes('geometry') || topicLower.includes('triangle') || topicLower.includes('circle')) {
      return [
        'Pythagorean theorem',
        'Trigonometry basics',
        'Area and perimeter formulas',
        'Coordinate geometry',
        'Geometric proofs'
      ]
    } else if (topicLower.includes('statistics') || topicLower.includes('probability')) {
      return [
        'Descriptive statistics',
        'Normal distribution',
        'Hypothesis testing',
        'Correlation and regression',
        'Sampling and confidence intervals'
      ]
    }
    
    // Physics topics
    else if (topicLower.includes('energy') || topicLower.includes('kinetic') || topicLower.includes('potential')) {
      return [
        'Conservation of energy',
        'Work and power',
        'Thermodynamics basics',
        'Heat transfer mechanisms',
        'Renewable energy sources'
      ]
    } else if (topicLower.includes('wave') || topicLower.includes('frequency')) {
      return [
        'Sound waves and acoustics',
        'Light waves and optics',
        'Electromagnetic spectrum',
        'Wave interference',
        'Doppler effect'
      ]
    } else if (topicLower.includes('electric') || topicLower.includes('current') || topicLower.includes('voltage')) {
      return [
        'Ohm\'s law and resistance',
        'Magnetism and electromagnetism',
        'Electric circuits',
        'Power and energy in circuits',
        'AC vs DC current'
      ]
    }
    
    // Chemistry topics
    else if (topicLower.includes('chemical') || topicLower.includes('reaction') || topicLower.includes('bond')) {
      return [
        'Types of chemical reactions',
        'Balancing chemical equations',
        'Acids and bases',
        'Oxidation and reduction',
        'Chemical equilibrium'
      ]
    } else if (topicLower.includes('periodic table') || topicLower.includes('element')) {
      return [
        'Atomic structure',
        'Electron configuration',
        'Chemical bonding',
        'Metallic and nonmetallic properties',
        'Noble gases and reactivity'
      ]
    }
    
    // History and Social Sciences
    else if (topicLower.includes('democracy') || topicLower.includes('government')) {
      return [
        'Types of government systems',
        'Constitutional principles',
        'Voting and elections',
        'Separation of powers',
        'Civil rights and liberties'
      ]
    } else if (topicLower.includes('economy') || topicLower.includes('economic')) {
      return [
        'Supply and demand',
        'Market structures',
        'Inflation and deflation',
        'Fiscal and monetary policy',
        'International trade'
      ]
    }
    
    // Biology topics
    else if (topicLower.includes('cell') || topicLower.includes('cellular')) {
      return [
        'Cell membrane and transport',
        'Mitosis and meiosis',
        'Organelles and their functions',
        'Prokaryotes vs eukaryotes',
        'Cell cycle regulation'
      ]
    } else if (topicLower.includes('ecosystem') || topicLower.includes('environment')) {
      return [
        'Food chains and webs',
        'Biodiversity and conservation',
        'Climate change effects',
        'Nutrient cycles',
        'Population dynamics'
      ]
    }
    
    // Default: Try to generate contextually appropriate topics
    else {
      // Extract key concepts and generate relevant topics
      const keywords = topicLower.split(/\s+/).filter(word => word.length > 3)
      const mainKeyword = keywords[0] || topic
      
      if (keywords.some(word => ['how', 'what', 'why', 'explain', 'define'].includes(word))) {
        return [
          `Advanced ${mainKeyword} concepts`,
          `${mainKeyword} in real-world applications`,
          `Common misconceptions about ${mainKeyword}`,
          `${mainKeyword} vs related concepts`,
          `Future developments in ${mainKeyword}`
        ]
      } else {
        return [
          `Fundamentals of ${mainKeyword}`,
          `Types and classifications of ${mainKeyword}`,
          `${mainKeyword} mechanisms and processes`,
          `Practical applications of ${mainKeyword}`,
          `Recent advances in ${mainKeyword}`
        ]
      }
    }
  }

  const handleQuizSubmissionInternal = async (formattedAnswers: any[], quizId: string) => {
    // Start streaming for quiz evaluation
    const streamingId = Date.now().toString()
    setCurrentStreamingId(streamingId)
    
    addStreamingStep({
      type: 'grading',
      content: 'Evaluating your answers...',
      brief: 'Checking each answer against the correct solutions',
      status: 'active'
    })

    await sleep(600)

    addStreamingStep({
      type: 'grading',
      content: 'Calculating your score...',
      brief: 'Computing your overall performance and identifying areas for improvement',
      status: 'active'
    })

    await sleep(500)

    addStreamingStep({
      type: 'grading',
      content: 'Preparing detailed feedback...',
      brief: 'Creating personalized explanations for each question to help you learn',
      status: 'active'
    })

    try {
      const response = await fetch('http://localhost:8000/api/quiz/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          quiz_id: quizId, 
          answers: formattedAnswers 
        })
      })

      const result = await response.json()
      
      addStreamingStep({
        type: 'grading',
        content: `Quiz completed! Score: ${result.score.toFixed(0)}%`,
        brief: `Your learning assessment is complete with detailed feedback for each question`,
        status: 'completed'
      })

      await sleep(800)
      clearStreaming()
      
      let resultContent = `**🎉 Quiz Results**\n\n`
      resultContent += `**Score: ${result.score.toFixed(0)}%** (${result.correct_answers}/${result.total_questions} correct)\n\n`
      
      if (result.mastery_achieved) {
        resultContent += '🏆 **Excellent! You\'ve mastered this concept!**\n\n'
      } else if (result.score >= 70) {
        resultContent += '👏 **Good work! You\'re getting there.**\n\n'
      } else {
        resultContent += '📚 **Keep studying - you\'ll get it next time!**\n\n'
      }

      // Analyze specific mistakes for targeted feedback
      const incorrectAnswers = result.feedback.filter(f => !f.correct)
      const conceptGaps = []
      
      // Extract key concepts from wrong answers
      incorrectAnswers.forEach(feedback => {
        if (feedback.explanation) {
          const explanation = feedback.explanation.toLowerCase()
          if (explanation.includes('definition') || explanation.includes('meaning') || explanation.includes('term')) {
            conceptGaps.push('basic definitions')
          }
          if (explanation.includes('process') || explanation.includes('mechanism') || explanation.includes('how') || explanation.includes('steps')) {
            conceptGaps.push('understanding processes')
          }
          if (explanation.includes('application') || explanation.includes('example') || explanation.includes('use') || explanation.includes('real-world')) {
            conceptGaps.push('practical applications')
          }
          if (explanation.includes('relationship') || explanation.includes('connection') || explanation.includes('between') || explanation.includes('related')) {
            conceptGaps.push('concept relationships')
          }
          if (explanation.includes('formula') || explanation.includes('calculation') || explanation.includes('equation') || explanation.includes('mathematical')) {
            conceptGaps.push('mathematical concepts')
          }
        }
      })

      // Add detailed feedback
      result.feedback.forEach((feedback: any, index: number) => {
        resultContent += `**${index + 1}.** ${feedback.correct ? '✅' : '❌'} `
        if (feedback.correct_answer) {
          resultContent += `Correct answer: ${feedback.correct_answer}\n`
        }
        resultContent += `${feedback.explanation}\n\n`
      })
      
      // Generate specific recap and advice
      let recap = ''
      let advice = ''
      
      if (result.mastery_achieved) {
        recap = 'Outstanding performance! You demonstrated strong understanding across all key areas.'
        advice = 'Consider exploring advanced applications or teaching this concept to someone else to reinforce your mastery.'
      } else if (result.score >= 70) {
        recap = `Good progress! You got ${result.correct_answers} out of ${result.total_questions} questions correct.`
        if (conceptGaps.length > 0) {
          recap += ` Your main challenges were in ${[...new Set(conceptGaps)].slice(0, 2).join(' and ')}.`
        }
        advice = 'Focus on the areas you missed. '
        if (conceptGaps.includes('basic definitions')) {
          advice += 'Review key definitions and terminology. '
        }
        if (conceptGaps.includes('understanding processes')) {
          advice += 'Study the step-by-step processes and mechanisms. '
        }
        if (conceptGaps.includes('practical applications')) {
          advice += 'Look for real-world examples and applications. '
        }
        if (conceptGaps.includes('concept relationships')) {
          advice += 'Focus on how different concepts connect to each other. '
        }
        if (conceptGaps.includes('mathematical concepts')) {
          advice += 'Practice the mathematical relationships and formulas. '
        }
        if (advice === 'Focus on the areas you missed. ') {
          advice = 'Review the specific questions you missed and try to understand the reasoning behind each correct answer.'
        }
      } else {
        recap = `You're building your foundation! You got ${result.correct_answers} out of ${result.total_questions} questions correct.`
        if (conceptGaps.length > 0) {
          recap += ` The main areas to work on are ${[...new Set(conceptGaps)].slice(0, 3).join(', ')}.`
        }
        advice = 'Start with the fundamentals. '
        if (conceptGaps.includes('basic definitions')) {
          advice += 'Make sure you understand the core definitions first. '
        }
        if (conceptGaps.includes('understanding processes')) {
          advice += 'Break down complex processes into simple steps. '
        }
        advice += 'Use visual aids, create your own examples, and practice explaining concepts in simple terms.'
      }
      
      // Add recap and learning advice
      resultContent += `---\n\n**📈 Learning Recap:**\n${recap}\n\n`
      resultContent += `**🎯 Personalized Next Steps:**\n${advice}\n\n`
      
      // Specific study tips based on identified gaps
      if (result.score < 70) {
        resultContent += `**📝 Targeted Study Tips:**\n`
        if (conceptGaps.includes('basic definitions')) {
          resultContent += `• Create flashcards for key terms and definitions\n`
        }
        if (conceptGaps.includes('understanding processes')) {
          resultContent += `• Draw flowcharts or diagrams showing step-by-step processes\n`
        }
        if (conceptGaps.includes('practical applications')) {
          resultContent += `• Find real-world examples and case studies\n`
        }
        if (conceptGaps.includes('concept relationships')) {
          resultContent += `• Create concept maps showing how ideas connect\n`
        }
        if (conceptGaps.includes('mathematical concepts')) {
          resultContent += `• Practice calculations and work through example problems\n`
        }
        if (conceptGaps.length === 0) {
          resultContent += `• Review the explanations for questions you missed\n`
          resultContent += `• Try explaining concepts in your own words\n`
          resultContent += `• Look for patterns in your incorrect answers\n`
        }
        resultContent += `\n`
      } else {
        resultContent += `**🚀 Continue Building Mastery:**\n`
        if (conceptGaps.length > 0) {
          resultContent += `• Strengthen your understanding of ${[...new Set(conceptGaps)].slice(0, 2).join(' and ')}\n`
        }
        resultContent += `• Explore advanced applications of this concept\n`
        resultContent += `• Try teaching this concept to someone else\n`
        resultContent += `• Look for connections to related topics\n\n`
      }

      addMessage({
        type: 'assistant',
        content: resultContent
      })

      // Suggest related topics after quiz
      const lastTopic = messages.filter(m => m.metadata?.lastTopic).slice(-1)[0]?.metadata?.lastTopic
      if (lastTopic) {
        await suggestRelatedTopics(lastTopic)
      }

    } catch (error) {
      clearStreaming()
      addMessage({
        type: 'assistant',
        content: 'Sorry, I had trouble grading the quiz. Please try again.',
        isError: true
      })
    }
  }

  const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

  return (
    <div className="min-h-screen bg-matrix-bg text-matrix-text flex flex-col">
      {/* Header */}
      <nav className="border-b border-gray-700 p-4 flex-shrink-0">
        <div className="container mx-auto">
          <h1 className="text-xl font-bold matrix-text">🧠 AI Concept Explainer</h1>
          <p className="text-sm text-gray-400">Learning made simple with AI • Streaming mode</p>
        </div>
      </nav>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 messages-container">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.map((message) => (
            <ChatMessage 
              key={message.id} 
              message={message} 
              onQuizSubmit={message.isQuiz ? handleQuizSubmitFromInterface : undefined}
            />
          ))}
          
          {/* Streaming Steps (Active or Completed/Collapsible) */}
          {streamingSteps.length > 0 && (
            <div className="flex justify-start mb-4">
              <div className="max-w-3xl">
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-700 text-matrix-text flex items-center justify-center text-sm font-bold">
                    🧠
                  </div>
                  <div className="flex-1">
                    <div className="inline-block p-4 rounded-lg bg-gray-800 text-matrix-text">
                      {streamingCompleted && (
                        <button
                          onClick={() => setIsStreamingCollapsed(!isStreamingCollapsed)}
                          className="flex items-center space-x-2 text-sm text-gray-400 hover:text-matrix-accent transition-colors mb-3"
                        >
                          <span>{isStreamingCollapsed ? '▶️' : '▼'}</span>
                          <span>Thinking Process ({streamingSteps.length} steps)</span>
                        </button>
                      )}
                      
                      {(!streamingCompleted || !isStreamingCollapsed) && (
                        <div className={`${streamingCompleted ? 'border-t border-gray-600 pt-3' : ''}`}>
                          <div className="space-y-2">
                            {streamingSteps.map((step, index) => (
                              <div 
                                key={step.id}
                                className={`
                                  streaming-step flex items-center space-x-2 p-2 rounded
                                  ${step.status === 'active' && !streamingCompleted ? 'streaming-active thinking-glow' : ''}
                                  ${step.status === 'active' && !streamingCompleted ? 'animate-pulse' : 'animate-none'} 
                                  transition-all duration-300
                                `}
                              >
                                <span className="text-lg flex-shrink-0">
                                  {streamingCompleted || step.status === 'completed' ? '✅' : 
                                   step.status === 'error' ? '❌' : 
                                   step.type === 'processing' ? '🧠' :
                                   step.type === 'keywords' ? '📝' :
                                   step.type === 'sources' ? '🔍' :
                                   step.type === 'explanation' ? '🤖' :
                                   step.type === 'visual' ? '🎨' :
                                   step.type === 'finalizing' ? '✨' :
                                   step.type === 'quiz' ? '🎯' :
                                   step.type === 'grading' ? '📊' :
                                   step.type === 'topics' ? '🔗' : '⏳'}
                                </span>
                                <div className="flex-1">
                                  <div 
                                    className={`text-sm ${
                                      streamingCompleted || step.status === 'completed' ? 'text-green-400' :
                                      step.status === 'active' && !streamingCompleted ? 'text-matrix-accent font-medium' : 
                                      step.status === 'error' ? 'text-red-400' : 'text-gray-400'
                                    }`}
                                  >
                                    {step.content}
                                  </div>
                                  {step.brief && (
                                    <div className="text-xs text-gray-500 mt-1 pl-2">
                                      {step.brief}
                                    </div>
                                  )}
                                </div>
                                
                                {/* Loading dots for active steps */}
                                {step.status === 'active' && !streamingCompleted && (
                                  <div className="flex space-x-1 flex-shrink-0">
                                    <div className="w-1.5 h-1.5 bg-matrix-accent rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                    <div className="w-1.5 h-1.5 bg-matrix-accent rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                    <div className="w-1.5 h-1.5 bg-matrix-accent rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                          
                          {/* Progress bar - only show when actively streaming */}
                          {!streamingCompleted && (
                            <div className="mt-3 pt-2 border-t border-gray-700">
                              <div className="flex items-center space-x-2">
                                <div className="flex-1 bg-gray-700 rounded-full h-1.5">
                                  <div 
                                    className="bg-matrix-accent h-1.5 rounded-full transition-all duration-500 ease-out"
                                    style={{ 
                                      width: `${(streamingSteps.filter(s => s.status === 'completed').length / Math.max(streamingSteps.length, 1)) * 100}%` 
                                    }}
                                  ></div>
                                </div>
                                <span className="text-xs text-gray-400">
                                  {streamingSteps.filter(s => s.status === 'completed').length}/{streamingSteps.length}
                                </span>
                              </div>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                    
                    <div className="text-xs text-gray-500 mt-1 text-left">
                      {streamingCompleted ? 'AI thinking process completed' : 'Processing...'}
                    </div>
                  </div>
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
            placeholder={
              isLoading 
                ? "AI is processing..." 
                : "Type your concept or answer here..."
            }
          />
        </div>
      </div>
    </div>
  )
}

export default App