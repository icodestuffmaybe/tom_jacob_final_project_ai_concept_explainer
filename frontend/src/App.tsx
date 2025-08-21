import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import QueryInput from './components/QueryInput'
import ExplanationDisplay from './components/ExplanationDisplay'
import AuthForm from './components/AuthForm'
import ProgressDashboard from './components/ProgressDashboard'
import { AuthProvider, useAuth } from './hooks/useAuth'
import './App.css'

const MainApp: React.FC = () => {
  const { user, isLoading } = useAuth()
  const [currentExplanation, setCurrentExplanation] = useState<any>(null)

  if (isLoading) {
    return (
      <div className="min-h-screen bg-matrix-bg flex items-center justify-center">
        <div className="text-matrix-text text-xl">Loading...</div>
      </div>
    )
  }

  if (!user) {
    return <AuthForm />
  }

  return (
    <Router>
      <div className="min-h-screen bg-matrix-bg text-matrix-text">
        <nav className="border-b border-gray-700 p-4">
          <div className="container mx-auto flex justify-between items-center">
            <h1 className="text-2xl font-bold matrix-text">AI Concept Explainer</h1>
            <div className="flex space-x-4">
              <a href="/" className="hover:text-matrix-accent">Learn</a>
              <a href="/progress" className="hover:text-matrix-accent">Progress</a>
              <span className="text-gray-400">Welcome, {user.username}</span>
            </div>
          </div>
        </nav>

        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={
              <div className="max-w-4xl mx-auto space-y-8">
                <QueryInput onExplanationReceived={setCurrentExplanation} />
                {currentExplanation && (
                  <ExplanationDisplay explanation={currentExplanation} />
                )}
              </div>
            } />
            <Route path="/progress" element={<ProgressDashboard />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

const App: React.FC = () => {
  return (
    <AuthProvider>
      <MainApp />
    </AuthProvider>
  )
}

export default App