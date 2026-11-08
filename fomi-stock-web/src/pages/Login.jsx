import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import { useTheme } from '../theme/ThemeContext'
import { errorMessage } from '../api/client'
import { ErrorBox } from '../components/ui'
import { CheckIcon, LeafIcon, MoonIcon, SunIcon } from '../components/icons'

export default function Login() {
  const { login } = useAuth()
  const { theme, toggleTheme } = useTheme()
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
      <section className="login-hero">
        <div className="login-brand">
          <span className="brand-mark brand-mark-light">
            <LeafIcon size={24} />
          </span>
          <span>
            <strong>FOMI Stock</strong>
            <small>Gestion des engrais</small>
          </span>
        </div>

        <div className="login-hero-body">
          <h1>La logistique des engrais, enfin simplifiée.</h1>
          <p>
            Centralisez les dépôts, les tickets, les distributions et le suivi des
            agriculteurs dans une seule plateforme fiable et traçable.
          </p>
          <ul className="login-points">
            <li><CheckIcon size={16} /> Suivi en temps réel des stocks par province</li>
            <li><CheckIcon size={16} /> Traçabilité complète des mouvements et lots</li>
            <li><CheckIcon size={16} /> Notifications email aux agriculteurs</li>
          </ul>
        </div>

        <footer className="login-hero-footer">
          Ministère de l’Agriculture — République du Burundi
        </footer>
      </section>

      <section className="login-panel">
        <button
          className="icon-btn login-theme-toggle"
          onClick={toggleTheme}
          aria-label={theme === 'dark' ? 'Activer le thème clair' : 'Activer le thème sombre'}
          title={theme === 'dark' ? 'Thème clair' : 'Thème sombre'}
          type="button"
        >
          {theme === 'dark' ? <SunIcon size={19} /> : <MoonIcon size={19} />}
        </button>
        <form className="login-card" onSubmit={submit}>
          <div className="login-title">Bienvenue</div>
          <div className="login-sub">Connectez-vous à votre espace de travail.</div>

          <ErrorBox message={error} />

          <div className="login-fields">
            <label className="field">
              <span className="field-label">Nom d’utilisateur</span>
              <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                autoFocus
                autoComplete="username"
                placeholder="admin"
              />
            </label>
            <label className="field">
              <span className="field-label">Mot de passe</span>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
                placeholder="••••••••"
              />
            </label>
          </div>

          <button className="btn btn-block" disabled={loading || !username || !password}>
            {loading ? 'Connexion…' : 'Se connecter'}
          </button>

          <div className="login-separator" />

          <div className="login-footer-link">
            <Link to="/suivi">Suivre un ticket sans connexion</Link>
          </div>
        </form>
        <p className="login-copyright">© {new Date().getFullYear()} FOMI — Tous droits réservés</p>
      </section>
    </div>
  )
}
