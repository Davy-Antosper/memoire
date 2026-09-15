import { useState } from 'react'
import { api, errorMessage } from '../api/client'
import { Loading, ErrorBox, Badge } from '../components/ui'
import { Link } from 'react-router-dom'

const STATUT_TONES = {
  EN_ATTENTE_DE_VALIDATION: 'amber',
  ACTIF: 'green',
  REJETE: 'red',
  EXPIRE: 'neutral',
  PAYE: 'green',
  EN_ATTENTE: 'neutral',
  PARTIEL: 'amber',
  SERVI: 'green',
  RECLAMATION: 'red',
  ANNULE: 'neutral'
}

export default function Suivi() {
  const [numero, setNumero] = useState('')
  const [ticket, setTicket] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function search(e) {
    e.preventDefault()
    if (!numero.trim()) return
    setLoading(true)
    setError('')
    setTicket(null)
    try {
      const { data } = await api.get(`/api/public/tickets/${encodeURIComponent(numero.trim())}`)
      setTicket(data)
    } catch (err) {
      setError(errorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-wrap" style={{ background: 'var(--green-light)' }}>
      <div className="login-card" style={{ maxWidth: 520 }}>
        <div className="login-title">Suivi de ticket</div>
        <div className="login-sub">Consultez l’état de votre ticket d’engrais FOMI</div>

        <form onSubmit={search} className="row" style={{ marginBottom: 16 }}>
          <input
            value={numero}
            onChange={(e) => setNumero(e.target.value)}
            placeholder="Ex : TKT-2026-0001"
            style={{ flex: 1 }}
            autoFocus
          />
          <button className="btn" disabled={loading || !numero.trim()}>
            {loading ? 'Recherche…' : 'Rechercher'}
          </button>
        </form>

        <ErrorBox message={error} />

        {!loading && ticket && (
          <div className="card" style={{ margin: 0 }}>
            <div className="row" style={{ justifyContent: 'space-between' }}>
              <strong>{ticket.numeroTicket}</strong>
              <Badge tone={STATUT_TONES[ticket.statut]}>{ticket.statut}</Badge>
            </div>
            <table>
              <tbody>
                <tr><th>Agriculteur</th><td>{ticket.agriculteurNomComplet}</td></tr>
                <tr><th>Engrais</th><td>{ticket.engraisTypeNom} ({ticket.engraisTypeCode})</td></tr>
                <tr><th>Quantité commandée</th><td className="num">{ticket.quantiteCommandee} sacs</td></tr>
                <tr><th>Quantité servie</th><td className="num">{ticket.quantiteServie} sacs</td></tr>
                <tr><th>Reste à servir</th><td className="num">{ticket.quantiteRestante} sacs</td></tr>
                <tr><th>Date de paiement</th><td>{new Date(ticket.datePaiement).toLocaleDateString('fr-FR')}</td></tr>
                <tr><th>Dépôt de retrait</th><td>{ticket.depotRetraitCode}</td></tr>
              </tbody>
            </table>
          </div>
        )}

        <div style={{ textAlign: 'center', marginTop: 16 }}>
          <Link to="/login" className="btn outline">Se connecter</Link>
        </div>
      </div>
    </div>
  )
}
