import { useEffect, useState } from 'react'
import { api, downloadCsv, errorMessage } from '../api/client'
import { Loading, ErrorBox, SuccessBox, Badge, Field, useForm, Empty, Pagination } from '../components/ui'
import { useAuth } from '../auth/AuthContext'
import { DownloadIcon } from '../components/icons'

const TYPE_TONES = {
  RECEPTION_FOMI: 'green',
  TRANSFERT: 'amber',
  DISTRIBUTION: 'blue',
  AJUSTEMENT: 'neutral'
}

function nouvelleCleIdempotence() {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID()
  }
  // Repli pour les navigateurs anciens ou les contextes non sécurisés (HTTP).
  return `mvt-${Date.now()}-${Math.random().toString(16).slice(2)}-${Math.random().toString(16).slice(2)}`
}

export default function Mouvements() {
  const { user } = useAuth()
  // Réception : ADMIN + AGENT_LOGISTIQUE ; transfert : ADMIN uniquement (cf. SecurityConfig).
  const canReception = ['ADMIN', 'AGENT_LOGISTIQUE'].includes(user.role)
  const canTransfert = user.role === 'ADMIN'
  const canWrite = canReception || canTransfert
  const canExport = ['ADMIN', 'SUPERVISEUR', 'AGENT_ZONE', 'AGENT_LOGISTIQUE'].includes(user.role)
  const [data, setData] = useState(null)
  const [page, setPage] = useState(0)
  const [depots, setDepots] = useState([])
  const [lots, setLots] = useState([])
  const [engrais, setEngrais] = useState([])
  const [error, setError] = useState('')
  const [msg, setMsg] = useState('')
  const [tab, setTab] = useState('reception')
  const [lotNumero, setLotNumero] = useState('')
  const [lotOptions, setLotOptions] = useState([])
  const [form, set, setAll, reset] = useForm({
    lotId: null,
    quantite: null,
    depotSourceId: null,
    depotDestId: null,
    commentaire: '',
    idempotencyKey: nouvelleCleIdempotence()
  })

  useEffect(() => {
    load()
    api.get('/api/depots').then((r) => setDepots(r.data)).catch(() => {})
    api.get('/api/lots').then((r) => { setLots(r.data); setLotOptions(r.data) }).catch(() => {})
    api.get('/api/engrais-types').then((r) => setEngrais(r.data)).catch(() => {})
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page])

  function load() {
    setData(null)
    setError('')
    api.get('/api/mouvements', { params: { page, size: 50 } })
      .then((r) => setData(r.data))
      .catch((e) => setError(errorMessage(e)))
  }

  function searchLot(q) {
    setLotNumero(q)
    const exact = lots.find((l) => l.numeroLot === q.trim())
    if (exact) {
      setAll({ lotId: exact.id })
    } else {
      setAll({ lotId: null })
    }
    if (!q.trim()) { setLotOptions(lots); return }
    api.get('/api/lots/recherche', { params: { numero: q.trim() } })
      .then((r) => setLotOptions(r.data))
      .catch(() => setLotOptions(lots))
  }

  async function submit(e) {
    e.preventDefault()
    setMsg('')
    setError('')
    try {
      const base = {
        lotId: Number(form.lotId),
        quantite: Number(form.quantite),
        depotDestId: Number(form.depotDestId),
        commentaire: form.commentaire || undefined,
        idempotencyKey: form.idempotencyKey
      }
      const endpoint = tab === 'reception' ? '/api/mouvements/reception' : '/api/mouvements/transfert'
      const payload = tab === 'transfert' ? { ...base, depotSourceId: Number(form.depotSourceId) } : base
      const { data } = await api.post(endpoint, payload)
      const rows = Array.isArray(data) ? data : [data]
      setMsg(`${rows.length} mouvement(s) enregistré(s)`)
      // Régénérer la clé d'idempotence : sinon une réutilisation du formulaire
      // renverrait la même clé et le serveur considérerait l'opération comme déjà traitée.
      reset()
      setAll({ idempotencyKey: nouvelleCleIdempotence() })
      setLotNumero('')
      setPage(0)
      load()
    } catch (err) {
      setError(errorMessage(err))
    }
  }

  if (!data) return error ? <ErrorBox message={error} /> : <Loading />

  const list = data.content

  return (
    <>
      <SuccessBox message={msg} />
      <div className="row page-actions">
        <div>
          <h2 className="section-title">Mouvements de stock</h2>
          <p className="section-sub">Réceptions fournisseur, transferts et historique des opérations.</p>
        </div>
        {canExport && (
          <button
            className="btn outline"
            onClick={() =>
              downloadCsv('/api/export/mouvements.csv', undefined, 'mouvements.csv')
                .catch((e) => setError(errorMessage(e)))
            }
          >
            <DownloadIcon size={17} />
            Exporter CSV
          </button>
        )}
      </div>
      <ErrorBox message={error} />

      {canWrite && (
        <div className="card">
          <div className="row">
            <h2 style={{ margin: 0 }}>{tab === 'transfert' ? 'Nouveau transfert' : 'Nouvelle réception'}</h2>
            {canReception && canTransfert && (
              <div className="segmented">
                <button type="button" className={tab === 'reception' ? 'active' : ''} onClick={() => setTab('reception')}>Réception</button>
                <button type="button" className={tab === 'transfert' ? 'active' : ''} onClick={() => setTab('transfert')}>Transfert</button>
              </div>
            )}
          </div>
          <form onSubmit={submit}>
            <div className="form-grid">
              <Field label="Lot (numéro)">
                <input list="lot-list" value={lotNumero} onChange={(e) => searchLot(e.target.value)} required />
                <datalist id="lot-list">
                  {lotOptions.map((l) => <option key={l.id} value={l.numeroLot}>{l.engraisTypeCode}</option>)}
                </datalist>
              </Field>
              <Field label="Quantité (sacs)">
                <input type="number" min="1" value={form.quantite} onChange={set('quantite')} required />
              </Field>
              {tab === 'transfert' && (
                <Field label="Dépôt source">
                  <select value={form.depotSourceId || ''} onChange={set('depotSourceId')} required>
                    <option value="">—</option>
                    {depots.filter((d) => d.actif).map((d) => <option key={d.id} value={d.id}>{d.nom} ({d.code})</option>)}
                  </select>
                </Field>
              )}
              <Field label="Dépôt destination">
                <select value={form.depotDestId || ''} onChange={set('depotDestId')} required>
                  <option value="">—</option>
                  {depots.filter((d) => d.actif).map((d) => <option key={d.id} value={d.id}>{d.nom} ({d.code})</option>)}
                </select>
              </Field>
              <Field label="Commentaire">
                <input value={form.commentaire} onChange={set('commentaire')} />
              </Field>
            </div>
            <button className="btn">Enregistrer</button>
          </form>
        </div>
      )}

      <div className="card">
        <h2>Historique</h2>
        {list.length === 0 ? (
          <Empty />
        ) : (
          <table>
            <thead>
              <tr>
                <th>Type</th><th>Lot</th><th>Engrais</th><th>Source</th><th>Destination</th>
                <th className="num">Quantité</th><th>Agent</th><th>Date</th>
              </tr>
            </thead>
            <tbody>
              {list.map((m) => (
                <tr key={m.id}>
                  <td><Badge tone={TYPE_TONES[m.type]}>{m.type}</Badge></td>
                  <td>{m.lotNumero}</td>
                  <td>{m.engraisTypeCode}</td>
                  <td>{m.depotSourceCode || '—'}</td>
                  <td>{m.depotDestCode || '—'}</td>
                  <td className="num">{m.quantite}</td>
                  <td>{m.agentUsername}</td>
                  <td>{new Date(m.dateMouvement).toLocaleString('fr-FR')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        <Pagination page={data.number} totalPages={data.totalPages} onPage={setPage} />
      </div>
    </>
  )
}
