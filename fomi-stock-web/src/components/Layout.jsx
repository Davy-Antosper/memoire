import { useEffect, useState } from 'react'
import { NavLink, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import { useTheme } from '../theme/ThemeContext'
import {
  AlertIcon,
  AuditIcon,
  DashboardIcon,
  DepotIcon,
  DistributionIcon,
  FarmerIcon,
  LeafIcon,
  LogoutIcon,
  LotIcon,
  MenuIcon,
  CloseIcon,
  MoonIcon,
  MovementIcon,
  ReclamationIcon,
  SunIcon,
  TicketIcon,
  UsersIcon
} from './icons'

const ROLE_LABELS = {
  ADMIN: 'Administrateur',
  AGENT_ZONE: 'Agent zone',
  AGENT_COLLINE: 'Agent colline',
  SUPERVISEUR: 'Superviseur',
  AGENT_LOGISTIQUE: 'Agent logistique'
}

const MENU = [
  { to: '/', label: 'Tableau de bord', icon: DashboardIcon, roles: ['ADMIN', 'SUPERVISEUR'] },
  { to: '/depots', label: 'Dépôts', icon: DepotIcon, roles: ['ADMIN', 'AGENT_ZONE', 'SUPERVISEUR'] },
  { to: '/tickets', label: 'Tickets', icon: TicketIcon, roles: ['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE', 'SUPERVISEUR'] },
  { to: '/distributions', label: 'Distributions', icon: DistributionIcon, roles: ['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE'] },
  { to: '/agriculteurs', label: 'Agriculteurs', icon: FarmerIcon, roles: ['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE'] },
  { to: '/mouvements', label: 'Mouvements', icon: MovementIcon, roles: ['ADMIN', 'AGENT_ZONE', 'AGENT_LOGISTIQUE'] },
  { to: '/lots', label: 'Lots', icon: LotIcon, roles: ['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE', 'SUPERVISEUR', 'AGENT_LOGISTIQUE'] },
  { to: '/alertes', label: 'Alertes', icon: AlertIcon, roles: ['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE', 'SUPERVISEUR'] },
  { to: '/reclamations', label: 'Réclamations', icon: ReclamationIcon, roles: ['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE', 'SUPERVISEUR'] },
  { to: '/utilisateurs', label: 'Utilisateurs', icon: UsersIcon, roles: ['ADMIN'] },
  { to: '/audit-logs', label: "Journal d'audit", icon: AuditIcon, roles: ['ADMIN'] }
]

function initials(nom = '') {
  return nom
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0])
    .join('')
    .toUpperCase()
}

export default function Layout({ children }) {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const navigate = useNavigate()
  const location = useLocation()
  const [open, setOpen] = useState(false)

  const items = MENU.filter((m) => user && m.roles.includes(user.role))
  const current = items.find((m) => (m.to === '/' ? location.pathname === '/' : location.pathname.startsWith(m.to)))

  useEffect(() => {
    setOpen(false)
  }, [location.pathname])

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${open ? 'open' : ''}`}>
        <div className="sidebar-brand">
          <span className="brand-mark">
            <LeafIcon size={22} />
          </span>
          <span className="brand-text">
            <strong>FOMI Stock</strong>
            <small>Gestion des engrais</small>
          </span>
          <button className="icon-btn sidebar-close" onClick={() => setOpen(false)} aria-label="Fermer le menu">
            <CloseIcon size={20} />
          </button>
        </div>

        <nav className="sidebar-nav">
          <span className="nav-section">Navigation</span>
          {items.map((m) => {
            const Icon = m.icon
            return (
              <NavLink
                key={m.to}
                to={m.to}
                end={m.to === '/'}
                className={({ isActive }) => (isActive ? 'nav-item active' : 'nav-item')}
              >
                <Icon size={19} />
                <span>{m.label}</span>
              </NavLink>
            )
          })}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-user">
            <span className="avatar">{initials(user?.nomComplet)}</span>
            <span className="sidebar-user-text">
              <strong>{user?.nomComplet}</strong>
              <small>{ROLE_LABELS[user?.role] || user?.role}</small>
            </span>
          </div>
          <button className="btn sidebar-logout" onClick={handleLogout}>
            <LogoutIcon size={17} />
            Déconnexion
          </button>
        </div>
      </aside>

      {open && <button className="sidebar-backdrop" onClick={() => setOpen(false)} aria-label="Fermer le menu" />}

      <div className="main">
        <header className="topbar">
          <div className="topbar-left">
            <button className="icon-btn menu-btn" onClick={() => setOpen(true)} aria-label="Ouvrir le menu">
              <MenuIcon size={22} />
            </button>
            <div>
              <div className="page-eyebrow">Espace de travail</div>
              <h1 className="page-title">{current?.label || 'FOMI Stock'}</h1>
            </div>
          </div>
          <div className="topbar-right">
            <span className="user-chip">
              <span className="avatar avatar-sm">{initials(user?.nomComplet)}</span>
              <span className="user-chip-text">
                <strong>{user?.nomComplet}</strong>
                <small>{ROLE_LABELS[user?.role] || user?.role}</small>
              </span>
            </span>
            <button
              className="icon-btn"
              onClick={toggleTheme}
              aria-label={theme === 'dark' ? 'Activer le thème clair' : 'Activer le thème sombre'}
              title={theme === 'dark' ? 'Thème clair' : 'Thème sombre'}
            >
              {theme === 'dark' ? <SunIcon size={19} /> : <MoonIcon size={19} />}
            </button>
            <button className="icon-btn logout-btn" onClick={handleLogout} aria-label="Se déconnecter" title="Se déconnecter">
              <LogoutIcon size={19} />
            </button>
          </div>
        </header>

        <main className="content">{children}</main>
      </div>
    </div>
  )
}
