import { Navigate, Route, Routes, useLocation } from 'react-router-dom'
import { AuthProvider, useAuth } from './auth/AuthContext'
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

function RequireAuth({ children }) {
  const { user } = useAuth()
  const location = useLocation()
  if (!user) return <Navigate to="/login" state={{ from: location }} replace />
  return children
}

function Shell() {
  const { user } = useAuth()
  const location = useLocation()
  if (!user) return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/suivi" element={<Suivi />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
  if (location.pathname === '/login') return <Navigate to="/" replace />
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/depots" element={<Depots />} />
        <Route path="/tickets" element={<Tickets />} />
        <Route path="/distributions" element={<Distributions />} />
        <Route path="/agriculteurs" element={<Agriculteurs />} />
        <Route path="/mouvements" element={<Mouvements />} />
        <Route path="/alertes" element={<Alertes />} />
        <Route path="/utilisateurs" element={<Utilisateurs />} />
        <Route path="/lots" element={<Lots />} />
        <Route path="/audit-logs" element={<AuditLogs />} />
        <Route path="/suivi" element={<Suivi />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <Shell />
    </AuthProvider>
  )
}
