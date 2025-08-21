import React, { useState } from 'react'
import { useAuth } from '../hooks/useAuth'

const AuthForm: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true)
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    grade_level: 7,
  })
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const { login, register } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      if (isLogin) {
        await login(formData.username, formData.password)
      } else {
        await register(formData)
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Authentication failed')
    } finally {
      setIsLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  return (
    <div className="min-h-screen bg-matrix-bg flex items-center justify-center">
      <div className="zen-card rounded-lg p-8 max-w-md w-full mx-4">
        <h1 className="text-3xl font-bold text-center matrix-text mb-8">
          AI Concept Explainer
        </h1>
        
        <div className="flex mb-6">
          <button
            type="button"
            onClick={() => setIsLogin(true)}
            className={`flex-1 py-2 px-4 rounded-l-lg ${
              isLogin 
                ? 'bg-matrix-accent text-black' 
                : 'bg-gray-700 text-matrix-text hover:bg-gray-600'
            }`}
          >
            Login
          </button>
          <button
            type="button"
            onClick={() => setIsLogin(false)}
            className={`flex-1 py-2 px-4 rounded-r-lg ${
              !isLogin 
                ? 'bg-matrix-accent text-black' 
                : 'bg-gray-700 text-matrix-text hover:bg-gray-600'
            }`}
          >
            Register
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={formData.username}
              onChange={handleChange}
              required
              className="w-full p-3 bg-gray-800 text-matrix-text rounded-lg border border-gray-600 focus:border-matrix-accent focus:outline-none"
            />
          </div>

          {!isLogin && (
            <>
              <div>
                <input
                  type="email"
                  name="email"
                  placeholder="Email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full p-3 bg-gray-800 text-matrix-text rounded-lg border border-gray-600 focus:border-matrix-accent focus:outline-none"
                />
              </div>
              <div>
                <select
                  name="grade_level"
                  value={formData.grade_level}
                  onChange={handleChange}
                  required
                  className="w-full p-3 bg-gray-800 text-matrix-text rounded-lg border border-gray-600 focus:border-matrix-accent focus:outline-none"
                >
                  {[7, 8, 9, 10, 11, 12].map((grade) => (
                    <option key={grade} value={grade}>
                      Grade {grade}
                    </option>
                  ))}
                </select>
              </div>
            </>
          )}

          <div>
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
              className="w-full p-3 bg-gray-800 text-matrix-text rounded-lg border border-gray-600 focus:border-matrix-accent focus:outline-none"
            />
          </div>

          {error && (
            <div className="text-red-400 text-sm text-center">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 px-4 bg-matrix-accent text-black rounded-lg hover:bg-green-400 disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
          >
            {isLoading ? 'Processing...' : isLogin ? 'Login' : 'Register'}
          </button>
        </form>

        <p className="text-center text-gray-400 text-sm mt-6">
          {isLogin ? "Don't have an account?" : "Already have an account?"}{' '}
          <button
            type="button"
            onClick={() => setIsLogin(!isLogin)}
            className="text-matrix-accent hover:underline"
          >
            {isLogin ? 'Register here' : 'Login here'}
          </button>
        </p>
      </div>
    </div>
  )
}

export default AuthForm