import { createContext, useContext, useEffect, useState } from 'react'
import { api } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('fomi_user'))
    } catch {
      return null
    }
  })

  // Une réponse 401 (token expiré/révoqué) doit aussi vider l'état React,
  // sinon l'utilisateur reste visuellement connecté malgré la perte du token.
  useEffect(() => {
    const onUnauthorized = () => setUser(null)
    window.addEventListener('fomi:unauthorized', onUnauthorized)
    return () => window.removeEventListener('fomi:unauthorized', onUnauthorized)
  }, [])

  async function login(username, password) {
    const { data } = await api.post('/api/auth/login', { username, password })
    localStorage.setItem('fomi_token', data.token)
    localStorage.setItem('fomi_user', JSON.stringify(data))
    setUser(data)
    return data
  }

  function logout() {
    localStorage.removeItem('fomi_token')
    localStorage.removeItem('fomi_user')
    setUser(null)
  }

  return <AuthContext.Provider value={{ user, login, logout }}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}
