import { useEffect, useState } from 'react'
import { api, errorMessage } from '../api/client'
import { ErrorBox, SuccessBox, Field, useForm, Empty } from '../components/ui'

export default function Distributions() {
  const [depots, setDepots] = useState([])
  const [lots, setLots] = useState([])
  const [tickets, setTickets] = useState([])
  const [error, setError] = useState('')
  const [msg, setMsg] = useState('')
  const [distributions, setDistributions] = useState(null)
  const [ticketNumero, setTicketNumero] = useState('')
  const [selectedTicket, setSelectedTicket] = useState(null)
  const [saving, setSaving] = useState(false)
  const [form, set, setAll] = useForm({ ticketId: null, depotId: null, lotId: null, quantite: null, commentaire: '' })

  useEffect(() => {
    api.get('/api/depots').then((r) => setDepots(r.data)).catch(() => {})
    api.get('/api/lots').then((r) => setLots(r.data)).catch(() => {})
    api.get('/api/tickets', { params: { page: 0, size: 200 } })
      .then((r) => setTickets(r.data.content))
      .catch(() => {})
  }, [])

  function selectTicket(q) {
    setTicketNumero(q)
    // La recherche est insensible à la casse : l'agent peut saisir le numéro
    // imprimé sur le ticket sans se soucier des majuscules.
    const t = tickets.find((x) => x.numeroTicket?.toLowerCase() === q.trim().toLowerCase())
    if (t) {
      setAll({ ticketId: t.id })
      setSelectedTicket(t)
      loadTicket(t.id)
    } else {
      setAll({ ticketId: null })
      setSelectedTicket(null)
      setDistributions(null)
    }
  }

  async function distribuer(e) {
    e.preventDefault()
    setMsg('')
    setError('')
    setSaving(true)
    try {
      const payload = {
        ticketId: Number(form.ticketId),
        depotId: Number(form.depotId),
        quantite: Number(form.quantite),
        commentaire: form.commentaire || undefined
      }
      if (form.lotId) payload.lotId = Number(form.lotId)
      const { data } = await api.post('/api/distributions', payload)
      setMsg(`${data.length} distribution(s) enregistrée(s)`)
      if (form.ticketId) loadTicket(form.ticketId)
      // Le restant du ticket et le stock changent : on rafraîchit la liste
      // pour que le prochain retrait parte de chiffres à jour.
      api.get('/api/tickets', { params: { page: 0, size: 200 } })
        .then((r) => setTickets(r.data.content))
        .catch(() => {})
    } catch (err) {
      setError(errorMessage(err))
    } finally {
      setSaving(false)
    }
  }

  function loadTicket(id) {
    setDistributions(null)
    api.get(`/api/distributions/ticket/${id}`)
      .then((r) => setDistributions(r.data))
      .catch((e) => setError(errorMessage(e)))
  }

    return (
      <>
        <SuccessBox message={msg} />
        <h1>Distributions</h1>
      <ErrorBox message={error} />

      <form className="card" onSubmit={distribuer}>
        <h2>Enregistrer une distribution</h2>
        <div className="form-grid">
          <Field label="Ticket (numéro)">
            <input list="ticket-list" value={ticketNumero} onChange={(e) => selectTicket(e.target.value)} placeholder="TKT-2026-1247" required />
            <datalist id="ticket-list">
              {tickets.map((t) => <option key={t.id} value={t.numeroTicket}>{t.agriculteurNomComplet} · {t.engraisTypeCode} · restant {t.quantiteRestante}</option>)}
            </datalist>
            {selectedTicket && (
              <span className="muted">
                {selectedTicket.agriculteurNomComplet} · {selectedTicket.engraisTypeCode} · commandé {selectedTicket.quantiteCommandee} · restant {selectedTicket.quantiteRestante} · {selectedTicket.depotRetraitCode}
              </span>
            )}
          </Field>
          <Field label="Dépôt">
            <select value={form.depotId || ''} onChange={set('depotId')} required>
              <option value="">—</option>
              {depots.filter((d) => d.actif).map((d) => <option key={d.id} value={d.id}>{d.nom} ({d.code})</option>)}
            </select>
          </Field>
          <Field label="Lot (optionnel)">
            <select value={form.lotId || ''} onChange={set('lotId')}>
              <option value="">Automatique (FIFO)</option>
              {lots.map((l) => <option key={l.id} value={l.id}>{l.numeroLot} ({l.engraisTypeCode})</option>)}
            </select>
          </Field>
          <Field label="Quantité (sacs)">
            <input type="number" min="1" value={form.quantite} onChange={set('quantite')} required />
          </Field>
          <Field label="Commentaire">
            <input value={form.commentaire} onChange={set('commentaire')} />
          </Field>
        </div>
        <button className="btn" disabled={saving}>{saving ? 'Enregistrement...' : 'Distribuer'}</button>
      </form>

      <div className="card">
        <h2>Distributions d'un ticket</h2>
        <p className="section-sub">
          Sélectionnez un ticket dans le formulaire ci-dessus pour afficher l'historique de ses retraits.
        </p>
        {!selectedTicket && <Empty label="Aucun ticket sélectionné" />}
        {selectedTicket && distributions &&
          (distributions.length === 0 ? (
            <Empty label={`Aucune distribution pour le ticket ${selectedTicket.numeroTicket}`} />
          ) : (
            <table>
              <thead>
                <tr><th>Ticket</th><th>Lot</th><th>Dépôt</th><th className="num">Quantité</th><th>Agent</th><th>Date</th></tr>
              </thead>
              <tbody>
                {distributions.map((d) => (
                  <tr key={d.id}>
                    <td>{d.ticketNumero}</td><td>{d.lotNumero}</td><td>{d.depotCode}</td>
                    <td className="num">{d.quantite}</td><td>{d.agentUsername}</td>
                    <td>{new Date(d.dateDistribution).toLocaleString('fr-FR')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ))}
      </div>
    </>
  )
}
