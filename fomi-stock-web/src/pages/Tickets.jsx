import { useEffect, useState } from 'react'
import { api, downloadCsv, errorMessage } from '../api/client'
import { Loading, ErrorBox, SuccessBox, Badge, Empty, Field, useForm, Pagination } from '../components/ui'
import { useAuth } from '../auth/AuthContext'

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

export default function Tickets() {
  const { user } = useAuth()
  const canEdit = user.role === 'ADMIN' || user.role === 'AGENT_ZONE'
  const canValidate = user.role === 'ADMIN' || user.role === 'SUPERVISEUR'
  const canExport = ['ADMIN', 'SUPERVISEUR', 'AGENT_ZONE', 'AGENT_LOGISTIQUE'].includes(user.role)
  const [data, setData] = useState(null)
  const [depots, setDepots] = useState([])
  const [engrais, setEngrais] = useState([])
  const [statut, setStatut] = useState('')
  const [page, setPage] = useState(0)
  const [error, setError] = useState('')
  const [selected, setSelected] = useState(null)
  const [distributions, setDistributions] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState(null)
  const [telephone, setTelephone] = useState('')
  const [agriculteurs, setAgriculteurs] = useState([])
  const [msg, setMsg] = useState('')
  const [rejeterTicket, setRejeterTicket] = useState(null)
  const [motif, setMotif] = useState('')
  const [form, set, setAll, reset] = useForm({
    numeroTicket: '',
    agriculteurId: null,
    engraisTypeId: null,
    quantiteCommandee: null,
    montantPaye: null,
    datePaiement: '',
    depotRetraitId: null
  })

  useEffect(() => {
    api.get('/api/depots').then((r) => setDepots(r.data)).catch(() => {})
    api.get('/api/engrais-types').then((r) => setEngrais(r.data)).catch(() => {})
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    setData(null)
    api.get('/api/tickets', { params: { ...(statut ? { statut } : {}), page, size: 50 } })
      .then((r) => setData(r.data))
      .catch((e) => setError(errorMessage(e)))
  }, [statut, page])

  function searchAgriculteur() {
    if (!telephone.trim()) return
    api.get('/api/agriculteurs/recherche', { params: { telephone: telephone.trim() } })
      .then((r) => setAgriculteurs(r.data))
      .catch((e) => setError(errorMessage(e)))
  }

  function openTicket(t) {
    setSelected(t)
    setDistributions(null)
    api.get(`/api/distributions/ticket/${t.id}`)
      .then((r) => setDistributions(r.data))
      .catch((e) => setError(errorMessage(e)))
  }

  function startCreate() {
    setEditing(null)
    reset()
    setShowForm(true)
  }

  function startEdit(t) {
    setEditing(t)
    setForm({})
    setAll({
      numeroTicket: t.numeroTicket,
      agriculteurId: t.agriculteurId,
      engraisTypeId: engrais.find((e) => e.code === t.engraisTypeCode)?.id || null,
      quantiteCommandee: t.quantiteCommandee,
      montantPaye: t.montantPaye,
      datePaiement: t.datePaiement,
      depotRetraitId: depots.find((d) => d.code === t.depotRetraitCode)?.id || null
    })
    setShowForm(true)
  }

  async function submit(e) {
    e.preventDefault()
    setMsg('')
    setError('')
    try {
      const payload = {
        numeroTicket: form.numeroTicket,
        agriculteurId: Number(form.agriculteurId),
        engraisTypeId: Number(form.engraisTypeId),
        quantiteCommandee: Number(form.quantiteCommandee),
        montantPaye: Number(form.montantPaye),
        datePaiement: form.datePaiement,
        depotRetraitId: Number(form.depotRetraitId)
      }
      const { data: saved } = editing
        ? await api.put(`/api/tickets/${editing.id}`, payload)
        : await api.post('/api/tickets', payload)
      setMsg(`Ticket ${saved.numeroTicket} ${editing ? 'modifié' : 'créé'}`)
      setShowForm(false)
      setEditing(null)
      api.get('/api/tickets', { params: { ...(statut ? { statut } : {}), page, size: 50 } })
        .then((r) => setData(r.data))
        .catch(() => {})
    } catch (err) {
      setError(errorMessage(err))
    }
  }

  function refresh() {
    api.get('/api/tickets', { params: { ...(statut ? { statut } : {}), page, size: 50 } })
      .then((r) => setData(r.data))
      .catch((e) => setError(errorMessage(e)))
  }

  async function activer(t) {
    setMsg('')
    setError('')
    try {
      const { data: saved } = await api.patch(`/api/tickets/${t.id}/activer`)
      setMsg(`Ticket ${saved.numeroTicket} activé`)
      refresh()
    } catch (err) {
      setError(errorMessage(err))
    }
  }

  async function rejeter() {
    if (!rejeterTicket) return
    setMsg('')
    setError('')
    try {
      const { data: saved } = await api.patch(`/api/tickets/${rejeterTicket.id}/rejeter`, {
        motif: motif || undefined
      })
      setMsg(`Ticket ${saved.numeroTicket} rejeté`)
      setRejeterTicket(null)
      setMotif('')
      refresh()
    } catch (err) {
      setError(errorMessage(err))
    }
  }

  if (error) return <ErrorBox message={error} />
  if (!data) return <Loading />

  return (
    <>
      <SuccessBox message={msg} />
      <div className="row">
        <h1 style={{ margin: 0 }}>Tickets</h1>
        {user.role !== 'SUPERVISEUR' && (
          <button className="btn" onClick={startCreate}>
            {showForm ? 'Annuler' : 'Nouveau ticket'}
          </button>
        )}
        {canExport && (
          <button
            className="btn outline"
            onClick={() =>
              downloadCsv('/api/export/tickets.csv', { statut: statut || undefined }, 'tickets.csv')
                .catch((e) => setError(errorMessage(e)))
            }
          >
            Exporter CSV
          </button>
        )}
      </div>

      <div className="filter-bar">
        <select value={statut} onChange={(e) => { setStatut(e.target.value); setPage(0) }}>
          <option value="">Tous les statuts</option>
          {Object.keys(STATUT_TONES).map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
        <span className="muted">{data.totalElements} ticket(s)</span>
      </div>

      {showForm && (
        <form className="card" onSubmit={submit}>
          <h2>{editing ? `Modifier ${editing.numeroTicket}` : 'Nouveau ticket'}</h2>
          <div className="form-grid">
            <Field label="Numéro du ticket">
              <input value={form.numeroTicket} onChange={set('numeroTicket')} placeholder="TKT-2026-0001" required disabled={!!editing} />
            </Field>
            <Field label="Quantité (sacs)">
              <input type="number" min="1" value={form.quantiteCommandee} onChange={set('quantiteCommandee')} required />
            </Field>
            <Field label="Montant payé (BIF)">
              <input type="number" min="0" step="0.01" value={form.montantPaye} onChange={set('montantPaye')} required />
            </Field>
            <Field label="Date de paiement">
              <input type="date" value={form.datePaiement} onChange={set('datePaiement')} required />
            </Field>
            <Field label="Engrais">
              <select value={form.engraisTypeId || ''} onChange={set('engraisTypeId')} required>
                <option value="">—</option>
                {engrais.map((e) => <option key={e.id} value={e.id}>{e.nom} ({e.code})</option>)}
              </select>
            </Field>
            <Field label="Dépôt de retrait">
              <select value={form.depotRetraitId || ''} onChange={set('depotRetraitId')} required>
                <option value="">—</option>
                {depots.filter((d) => d.actif).map((d) => <option key={d.id} value={d.id}>{d.nom} ({d.code})</option>)}
              </select>
            </Field>
            {!editing && (
              <>
                <Field label="Rechercher l'agriculteur (téléphone)">
                  <div style={{ display: 'flex', gap: 6 }}>
                    <input value={telephone} onChange={(e) => setTelephone(e.target.value)} placeholder="79000001" />
                    <button type="button" className="btn outline" onClick={searchAgriculteur}>Rechercher</button>
                  </div>
                </Field>
                <Field label="Agriculteur">
                  <select value={form.agriculteurId || ''} onChange={set('agriculteurId')} required>
                    <option value="">—</option>
                    {agriculteurs.map((a) => (
                      <option key={a.id} value={a.id}>{a.nom} {a.prenom} — {a.numeroIdentite}</option>
                    ))}
                  </select>
                </Field>
              </>
            )}
          </div>
          <button className="btn">{editing ? 'Enregistrer les modifications' : 'Créer le ticket'}</button>
        </form>
      )}

      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Numéro</th><th>Agriculteur</th><th>Engrais</th>
              <th className="num">Qté</th><th className="num">Servi</th><th>Statut</th><th></th>
            </tr>
          </thead>
          <tbody>
            {data.content.length === 0 && <tr><td colSpan={7}><Empty /></td></tr>}
            {data.content.map((t) => (
              <tr key={t.id}>
                <td><strong>{t.numeroTicket}</strong></td>
                <td>{t.agriculteurNomComplet}</td>
                <td>{t.engraisTypeCode}</td>
                <td className="num">{t.quantiteCommandee}</td>
                <td className="num">{t.quantiteServie}</td>
                <td><Badge tone={STATUT_TONES[t.statut]}>{t.statut}</Badge></td>
                <td>
                  <button className="btn outline" onClick={() => openTicket(t)}>Détails</button>{' '}
                  {canEdit && t.quantiteServie === 0 && (
                    <button className="btn outline" onClick={() => startEdit(t)}>Modifier</button>
                  )}{' '}
                  {canValidate && t.statut === 'EN_ATTENTE_DE_VALIDATION' && (
                    <>
                      <button className="btn outline" onClick={() => activer(t)}>Activer</button>{' '}
                      <button className="btn danger" onClick={() => { setRejeterTicket(t); setMotif('') }}>
                        Rejeter
                      </button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <Pagination page={data.number} totalPages={data.totalPages} onPage={setPage} />
      </div>

      {selected && (
        <div className="card">
          <h2>Ticket {selected.numeroTicket} — {selected.agriculteurNomComplet}</h2>
          <p className="muted">
            Engrais {selected.engraisTypeCode} · Commandé {selected.quantiteCommandee} sacs · Servi {selected.quantiteServie} ·
            Restant {selected.quantiteRestante} · Payé {selected.montantPaye.toLocaleString('fr-FR')} BIF · Retrait {selected.depotRetraitCode}
          </p>
          {!distributions ? (
            <Loading />
          ) : distributions.length === 0 ? (
            <Empty label="Aucune distribution pour ce ticket" />
          ) : (
            <table>
              <thead>
                <tr><th>Lot</th><th>Dépôt</th><th className="num">Quantité</th><th>Agent</th><th>Date</th></tr>
              </thead>
              <tbody>
                {distributions.map((d) => (
                  <tr key={d.id}>
                    <td>{d.lotNumero}</td><td>{d.depotCode}</td>
                    <td className="num">{d.quantite}</td><td>{d.agentUsername}</td>
                    <td>{new Date(d.dateDistribution).toLocaleString('fr-FR')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {rejeterTicket && (
        <div className="card" style={{ borderColor: 'var(--red)' }}>
          <h2>Rejeter le ticket {rejeterTicket.numeroTicket}</h2>
          <Field label="Motif du rejet (optionnel)">
            <textarea
              value={motif}
              onChange={(e) => setMotif(e.target.value)}
              placeholder="Ex : paiement non confirmé…"
              rows={3}
            />
          </Field>
          <div className="row">
            <button className="btn danger" onClick={rejeter}>Confirmer le rejet</button>
            <button className="btn outline" onClick={() => { setRejeterTicket(null); setMotif('') }}>Annuler</button>
          </div>
        </div>
      )}
    </>
  )
}
