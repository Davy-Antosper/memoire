import { Navigate, Route, Routes, useLocation } from 'react-router-dom'
import { AuthProvider, useAuth } from './auth/AuthContext'
import { ThemeProvider } from './theme/ThemeContext'
import Layout from './components/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Depots from './pages/Depots'
import Tickets from './pages/Tickets'
import Distributions from './pages/Distributions'
import Agriculteurs from './pages/Agriculteurs'
import Mouvements from './pages/Mouvements'
import Alertes from './pages/Alertes'
import Utilisateurs from './pages/Utilisateurs'
import Lots from './pages/Lots'
import Suivi from './pages/Suivi'
import AuditLogs from './pages/AuditLogs'

const DASHBOARD_ROLES = ['ADMIN', 'SUPERVISEUR']

function homeFor(user) {
  if (!user) return '/login'
  if (DASHBOARD_ROLES.includes(user.role)) return '/'
  if (user.role === 'AGENT_LOGISTIQUE') return '/mouvements'
  return '/tickets'
}

function RequireRole({ roles, children }) {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  if (!roles.includes(user.role)) return <Navigate to={homeFor(user)} replace />
  return children
}

function Home() {
  const { user } = useAuth()
  if (DASHBOARD_ROLES.includes(user.role)) return <Dashboard />
  return <Navigate to={homeFor(user)} replace />
}

function Shell() {
  const { user } = useAuth()
  const location = useLocation()
  if (!user) {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/suivi" element={<Suivi />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    )
  }
  if (location.pathname === '/login') return <Navigate to={homeFor(user)} replace />
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/depots" element={<RequireRole roles={['ADMIN', 'AGENT_ZONE', 'SUPERVISEUR']}><Depots /></RequireRole>} />
        <Route path="/tickets" element={<RequireRole roles={['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE', 'SUPERVISEUR']}><Tickets /></RequireRole>} />
        <Route path="/distributions" element={<RequireRole roles={['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE']}><Distributions /></RequireRole>} />
        <Route path="/agriculteurs" element={<RequireRole roles={['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE']}><Agriculteurs /></RequireRole>} />
        <Route path="/mouvements" element={<RequireRole roles={['ADMIN', 'AGENT_ZONE', 'AGENT_LOGISTIQUE']}><Mouvements /></RequireRole>} />
        <Route path="/alertes" element={<RequireRole roles={['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE', 'SUPERVISEUR']}><Alertes /></RequireRole>} />
        <Route path="/utilisateurs" element={<RequireRole roles={['ADMIN']}><Utilisateurs /></RequireRole>} />
        <Route path="/lots" element={<Lots />} />
        <Route path="/audit-logs" element={<RequireRole roles={['ADMIN']}><AuditLogs /></RequireRole>} />
        <Route path="/suivi" element={<Suivi />} />
        <Route path="*" element={<Navigate to={homeFor(user)} replace />} />
      </Routes>
    </Layout>
  )
}

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Shell />
      </AuthProvider>
    </ThemeProvider>
  )
}
