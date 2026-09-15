import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

const ROLE_LABELS = {
  ADMIN: 'Administrateur',
  AGENT_ZONE: 'Agent zone',
  AGENT_COLLINE: 'Agent colline',
  SUPERVISEUR: 'Superviseur',
  AGENT_LOGISTIQUE: 'Agent logistique'
}

const MENU = [
  { to: '/', label: 'Tableau de bord', roles: ['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE', 'SUPERVISEUR'] },
  { to: '/depots', label: 'Dépôts', roles: ['ADMIN', 'AGENT_ZONE', 'SUPERVISEUR'] },
  { to: '/tickets', label: 'Tickets', roles: ['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE', 'SUPERVISEUR'] },
  { to: '/distributions', label: 'Distributions', roles: ['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE'] },
  { to: '/agriculteurs', label: 'Agriculteurs', roles: ['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE'] },
  { to: '/mouvements', label: 'Mouvements', roles: ['ADMIN', 'AGENT_ZONE', 'AGENT_LOGISTIQUE'] },
  { to: '/lots', label: 'Lots', roles: ['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE', 'SUPERVISEUR', 'AGENT_LOGISTIQUE'] },
  { to: '/alertes', label: 'Alertes', roles: ['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE', 'SUPERVISEUR'] },
  { to: '/utilisateurs', label: 'Utilisateurs', roles: ['ADMIN'] },
  { to: '/audit-logs', label: 'Logs d’audit', roles: ['ADMIN'] }
]

export default function Layout({ children }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const items = MENU.filter((m) => user && m.roles.includes(user.role))

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <span className="brand-dot" />
          Fomi Stock
        </div>
        <div className="topbar-right">
          <span className="user-chip">
            <span className="user-name">{user?.nomComplet}</span>
            <span className="user-role">{ROLE_LABELS[user?.role]}</span>
          </span>
          <button
            className="btn ghost"
            onClick={() => {
              logout()
              navigate('/login')
            }}
          >
            Déconnexion
          </button>
        </div>
      </header>

      <div className="body">
        <nav className="sidebar">
          {items.map((m) => (
            <NavLink
              key={m.to}
              to={m.to}
              className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}
            >
              {m.label}
            </NavLink>
          ))}
        </nav>
        <main className="content">{children}</main>
      </div>
    </div>
  )
}
