import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import { errorMessage } from '../api/client'
import { ErrorBox } from '../components/ui'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function submit(e) {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      await login(username, password)
      navigate('/')
    } catch (err) {
      setError(errorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-wrap">
      <form className="login-card" onSubmit={submit}>
        <div className="login-title">Fomi Stock</div>
        <div className="login-sub">Gestion des stocks d’engrais FOMI</div>
        <ErrorBox message={error} />
        <div className="form-grid" style={{ gridTemplateColumns: '1fr' }}>
          <label className="field">
            <span className="field-label">Nom d’utilisateur</span>
            <input value={username} onChange={(e) => setUsername(e.target.value)} autoFocus autoComplete="username" />
          </label>
          <label className="field">
            <span className="field-label">Mot de passe</span>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} autoComplete="current-password" />
          </label>
        </div>
        <button className="btn" disabled={loading || !username || !password} style={{ width: '100%' }}>
          {loading ? 'Connexion…' : 'Se connecter'}
        </button>
        <div style={{ textAlign: 'center', marginTop: 12 }}>
          <Link to="/suivi">Suivre un ticket sans connexion</Link>
        </div>
      </form>
    </div>
  )
}
