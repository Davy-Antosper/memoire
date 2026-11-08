import { useEffect, useState } from 'react'
import { api, errorMessage } from '../api/client'
import { Loading, ErrorBox, SuccessBox, Badge, Empty, Field, useForm } from '../components/ui'
import { useAuth } from '../auth/AuthContext'
import { PlusIcon, SearchIcon } from '../components/icons'

const STATUT_TONES = {
  OUVERTE: 'amber',
  EN_INSTRUCTION: 'blue',
  RESOLUE: 'green',
  REJETEE: 'red'
}

const STATUT_LABELS = {
  OUVERTE: 'Ouverte',
  EN_INSTRUCTION: 'En instruction',
  RESOLUE: 'Résolue',
  REJETEE: 'Rejetée'
}

const MOTIFS = [
  'Engrais payé non retiré',
  'Quantité servie incomplète',
  'Paiement non pris en compte',
  'Engrais de mauvaise qualité',
  'Autre'
]

export default function Reclamations() {
  const { user } = useAuth()
  const canCreer = ['ADMIN', 'AGENT_ZONE', 'AGENT_COLLINE'].includes(user.role)
  const canInstruire = ['ADMIN', 'SUPERVISEUR'].includes(user.role)

  const [list, setList] = useState(null)
  const [statut, setStatut] = useState('')
  const [error, setError] = useState('')
  const [msg, setMsg] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [tickets, setTickets] = useState([])
  const [recherche, setRecherche] = useState('')
  const [cloture, setCloture] = useState(null)
  const [resolution, setResolution] = useState('')
  const [saving, setSaving] = useState(false)
  const [busyId, setBusyId] = useState(null)
  const [form, set, reset] = useForm({
    ticketId: null,
    motif: MOTIFS[0],
    description: '',
    quantiteManquante: null
  })

  function load(currentStatut) {
    setList(null)
    setError('')
    api.get('/api/reclamations', { params: currentStatut ? { statut: currentStatut } : {} })
      .then((r) => setList(r.data))
      .catch((e) => setError(errorMessage(e)))
  }

  useEffect(() => {
    load(statut)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statut])

  useEffect(() => {
    api.get('/api/tickets', { params: { size: 100 } })
      .then((r) => setTickets(r.data.content || []))
      .catch(() => {})
  }, [])

  function startCreate() {
    setError('')
    setMsg('')
    reset()
    setShowForm(true)
  }

  async function submit(e) {
    e.preventDefault()
    setError('')
    setMsg('')
    setSaving(true)
    try {
      await api.post('/api/reclamations', {
        ticketId: Number(form.ticketId),
        motif: form.motif,
        description: form.description || null,
        quantiteManquante: form.quantiteManquante != null ? Number(form.quantiteManquante) : null
      })
      setMsg('Réclamation enregistrée.')
      setShowForm(false)
      reset()
      load(statut)
    } catch (err) {
      setError(errorMessage(err))
    } finally {
      setSaving(false)
    }
  }

  async function changerStatut(id, nouveau, texte) {
    setError('')
    setMsg('')
    setBusyId(id)
    try {
      await api.patch(`/api/reclamations/${id}/statut`, {
        statut: nouveau,
        resolution: texte || null
      })
      setMsg(`Réclamation passée en « ${STATUT_LABELS[nouveau] || nouveau} ».`)
      setCloture(null)
      setResolution('')
      load(statut)
    } catch (err) {
      setError(errorMessage(err))
    } finally {
      setBusyId(null)
    }
  }

  const ticketsFiltres = recherche.trim()
    ? tickets.filter((t) => {
        const q = recherche.trim().toLowerCase()
        return (
          (t.numeroTicket || '').toLowerCase().includes(q) ||
          (t.agriculteurNomComplet || '').toLowerCase().includes(q)
        )
      })
    : tickets

  if (!list) return error ? <ErrorBox message={error} /> : <Loading />

  return (
    <>
      <SuccessBox message={msg} />
      <ErrorBox message={error} />

      <div className="page-actions">
        <div>
          <h2 className="section-title">Réclamations</h2>
          <p className="section-sub">
            Litiges liés aux tickets : engrais payé non retiré, quantité incomplète, paiement contesté.
          </p>
        </div>
        {canCreer && (
          <button className="btn" onClick={() => (showForm ? setShowForm(false) : startCreate())}>
            <PlusIcon size={17} />
            {showForm ? 'Annuler' : 'Nouvelle réclamation'}
          </button>
        )}
      </div>

      <div className="filter-bar">
        <select value={statut} onChange={(e) => setStatut(e.target.value)}>
          <option value="">Tous les statuts</option>
          {Object.keys(STATUT_TONES).map((s) => (
            <option key={s} value={s}>{STATUT_LABELS[s]}</option>
          ))}
        </select>
        <span className="muted">{list.length} réclamation(s)</span>
      </div>

      {showForm && (
        <form className="card" onSubmit={submit}>
          <h2>Nouvelle réclamation</h2>
          <div className="form-grid">
            <Field label="Rechercher un ticket (numéro ou agriculteur)">
              <div style={{ display: 'flex', gap: 6 }}>
                <input
                  value={recherche}
                  onChange={(e) => setRecherche(e.target.value)}
                  placeholder="TKT-2026-0001"
                />
                <span className="btn outline" style={{ pointerEvents: 'none' }}>
                  <SearchIcon size={17} />
                </span>
              </div>
            </Field>
            <Field label="Ticket concerné">
              <select value={form.ticketId || ''} onChange={set('ticketId')} required>
                <option value="">—</option>
                {ticketsFiltres.map((t) => (
                  <option key={t.id} value={t.id}>
                    {t.numeroTicket} — {t.agriculteurNomComplet || ''} (reste {t.quantiteRestante ?? '—'} sacs)
                  </option>
                ))}
              </select>
            </Field>
            <Field label="Motif">
              <select value={form.motif} onChange={set('motif')} required>
                {MOTIFS.map((m) => <option key={m} value={m}>{m}</option>)}
              </select>
            </Field>
            <Field label="Quantité manquante (sacs, optionnel)">
              <input
                type="number"
                min="0"
                value={form.quantiteManquante ?? ''}
                onChange={set('quantiteManquante')}
                placeholder="Héritée du reste à servir si vide"
              />
            </Field>
            <Field label="Description (optionnel)">
              <textarea
                value={form.description || ''}
                onChange={set('description')}
                rows={3}
                maxLength={1000}
                placeholder="Circonstances, personnes rencontrées, dates…"
              />
            </Field>
          </div>
          <button className="btn" disabled={saving}>{saving ? 'Enregistrement...' : 'Enregistrer la réclamation'}</button>
          <button type="button" className="btn outline" onClick={() => setShowForm(false)}>Annuler</button>
        </form>
      )}

      {cloture && (
        <div className="card">
          <h2>
            {cloture.cible === 'RESOLUE' ? 'Résoudre' : 'Rejeter'} la réclamation #{cloture.item.id}
          </h2>
          <p className="muted">
            Ticket {cloture.item.ticketNumero} — {cloture.item.agriculteurNomComplet}
          </p>
          <Field label={cloture.cible === 'RESOLUE' ? 'Résolution (obligatoire)' : 'Motif du rejet (obligatoire)'}>
            <textarea
              value={resolution}
              onChange={(e) => setResolution(e.target.value)}
              rows={3}
              maxLength={1000}
              required
              placeholder={
                cloture.cible === 'RESOLUE'
                  ? 'Ex. : reliquat livré au dépôt de zone le 12/11, reçu signé.'
                  : 'Ex. : paiement non retrouvé au guichet de la Poste.'
              }
            />
          </Field>
          <button
            className="btn"
            disabled={!resolution.trim() || busyId !== null}
            onClick={() => changerStatut(cloture.item.id, cloture.cible, resolution)}
          >
            {busyId === cloture.item.id ? 'Enregistrement...' : 'Confirmer'}
          </button>
          <button
            className="btn outline"
            onClick={() => { setCloture(null); setResolution('') }}
          >
            Annuler
          </button>
        </div>
      )}

      <div className="card">
        {list.length === 0 ? (
          <Empty label="Aucune réclamation" />
        ) : (
          <table>
            <thead>
              <tr>
                <th>Ticket</th><th>Agriculteur</th><th>Motif</th>
                <th className="num">Manquant</th><th>Statut</th><th>Créée le</th><th></th>
              </tr>
            </thead>
            <tbody>
              {list.map((r) => (
                <tr key={r.id}>
                  <td>{r.ticketNumero}</td>
                  <td>{r.agriculteurNomComplet}</td>
                  <td>
                    {r.motif}
                    {r.description && <div className="muted" style={{ fontSize: '0.85em' }}>{r.description}</div>}
                    {r.resolution && <div className="muted" style={{ fontSize: '0.85em' }}>→ {r.resolution}</div>}
                  </td>
                  <td className="num">{r.quantiteManquante != null ? `${r.quantiteManquante} sacs` : '—'}</td>
                  <td><Badge tone={STATUT_TONES[r.statut] || 'neutral'}>{STATUT_LABELS[r.statut] || r.statut}</Badge></td>
                  <td>{new Date(r.dateCreation).toLocaleDateString('fr-FR')}</td>
                  <td>
                    {canInstruire && r.statut === 'OUVERTE' && (
                      <button
                        className="btn outline"
                        disabled={busyId !== null}
                        onClick={() => changerStatut(r.id, 'EN_INSTRUCTION')}
                      >
                        {busyId === r.id ? 'En cours...' : 'Prendre en charge'}
                      </button>
                    )}
                    {canInstruire && (r.statut === 'OUVERTE' || r.statut === 'EN_INSTRUCTION') && (
                      <>
                        <button
                          className="btn"
                          disabled={busyId !== null}
                          onClick={() => { setCloture({ item: r, cible: 'RESOLUE' }); setResolution(''); setError(''); setMsg('') }}
                        >
                          Résoudre
                        </button>
                        <button
                          className="btn danger"
                          disabled={busyId !== null}
                          onClick={() => { setCloture({ item: r, cible: 'REJETEE' }); setResolution(''); setError(''); setMsg('') }}
                        >
                          Rejeter
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  )
}
