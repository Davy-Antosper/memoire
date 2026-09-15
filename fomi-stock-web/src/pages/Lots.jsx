import { useEffect, useState } from 'react'
import { api, errorMessage } from '../api/client'
import { Loading, ErrorBox, SuccessBox, Empty, Field, useForm } from '../components/ui'
import { useAuth } from '../auth/AuthContext'

export default function Lots() {
  const { user } = useAuth()
  const [lots, setLots] = useState(null)
  const [engrais, setEngrais] = useState([])
  const [error, setError] = useState('')
  const [msg, setMsg] = useState('')
  const [q, setQ] = useState('')
  const [showCreate, setShowCreate] = useState(false)
  const [form, set] = useForm({ numeroLot: '', engraisTypeId: null, quantiteInitiale: '', dateFabrication: '', datePeremption: '' })

  function load(numero) {
    const url = numero && numero.trim() ? `/api/lots/recherche?numero=${encodeURIComponent(numero.trim())}` : '/api/lots'
    api.get(url).then((r) => setLots(r.data)).catch((e) => setError(errorMessage(e)))
  }

  useEffect(() => {
    load(q)
    api.get('/api/engrais-types').then((r) => setEngrais(r.data)).catch(() => {})
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function submit(e) {
    e.preventDefault()
    setMsg('')
    setError('')
    try {
      const { data } = await api.post('/api/lots', {
        numeroLot: form.numeroLot.trim(),
        engraisTypeId: Number(form.engraisTypeId),
        quantiteInitiale: Number(form.quantiteInitiale),
        dateFabrication: form.dateFabrication || null,
        datePeremption: form.datePeremption || null
      })
      setMsg(`Lot ${data.numeroLot} créé`)
      setShowCreate(false)
      setQ('')
      load('')
    } catch (err) {
      setError(errorMessage(err))
    }
  }

  function search(e) {
    const v = e.target.value
    setQ(v)
    load(v)
  }

  if (error) return <ErrorBox message={error} />
  if (!lots) return <Loading />

  return (
    <>
      <SuccessBox message={msg} />
      <div className="row">
        <h1 style={{ margin: 0 }}>Lots</h1>
        {['ADMIN', 'AGENT_LOGISTIQUE'].includes(user.role) && (
          <button className="btn outline" onClick={() => setShowCreate((v) => !v)}>
            {showCreate ? 'Annuler' : 'Nouveau lot'}
          </button>
        )}
      </div>

      {showCreate && (
        <form className="card" onSubmit={submit}>
          <h2>Nouveau lot</h2>
          <div className="form-grid">
            <Field label="Numéro de lot">
              <input value={form.numeroLot} onChange={set('numeroLot')} placeholder="LOT-UREE-2026-003" required />
            </Field>
            <Field label="Engrais">
              <select value={form.engraisTypeId || ''} onChange={set('engraisTypeId')} required>
                <option value="">—</option>
                {engrais.map((e) => <option key={e.id} value={e.id}>{e.nom} ({e.code})</option>)}
              </select>
            </Field>
            <Field label="Quantité initiale (sacs)">
              <input type="number" min="1" value={form.quantiteInitiale} onChange={set('quantiteInitiale')} required />
            </Field>
            <Field label="Date de fabrication">
              <input type="date" value={form.dateFabrication} onChange={set('dateFabrication')} />
            </Field>
            <Field label="Date de péremption">
              <input type="date" value={form.datePeremption} onChange={set('datePeremption')} />
            </Field>
          </div>
          <button className="btn">Créer le lot</button>
        </form>
      )}

      <div className="card">
        <div className="row" style={{ marginBottom: 12 }}>
          <h2 style={{ margin: 0 }}>Liste des lots</h2>
          <input
            placeholder="Rechercher un numéro de lot…"
            value={q}
            onChange={search}
            style={{ maxWidth: 260 }}
          />
        </div>
        {lots.length === 0 ? (
          <Empty />
        ) : (
          <table>
            <thead>
              <tr>
                <th>Numéro</th><th>Engrais</th><th className="num">Quantité initiale</th>
                <th>Fabrication</th><th>Péremption</th><th>Réception FOMI</th>
              </tr>
            </thead>
            <tbody>
              {lots.map((l) => (
                <tr key={l.id}>
                  <td><strong>{l.numeroLot}</strong></td>
                  <td>{l.engraisTypeNom} ({l.engraisTypeCode})</td>
                  <td className="num">{l.quantiteInitiale}</td>
                  <td>{l.dateFabrication || '—'}</td>
                  <td>{l.datePeremption || '—'}</td>
                  <td>{new Date(l.dateReceptionFomi).toLocaleDateString('fr-FR')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  )
}
