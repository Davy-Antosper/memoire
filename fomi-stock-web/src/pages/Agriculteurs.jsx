import { useEffect, useState } from 'react'
import { api, errorMessage } from '../api/client'
import { Loading, ErrorBox, SuccessBox, Empty, Field, useForm, Pagination } from '../components/ui'

export default function Agriculteurs() {
  const [data, setData] = useState(null)
  const [provinces, setProvinces] = useState([])
  const [zones, setZones] = useState([])
  const [collines, setCollines] = useState([])
  const [error, setError] = useState('')
  const [msg, setMsg] = useState('')
  const [telephone, setTelephone] = useState('')
  const [page, setPage] = useState(0)
  const [showCreate, setShowCreate] = useState(false)
  const [notifyFor, setNotifyFor] = useState(null)
  const [notifyForm, setNotifyForm] = useState({ sujet: '', message: '' })
  const [notifyError, setNotifyError] = useState('')
  const [form, set, setAll, reset] = useForm({
    numeroIdentite: '',
    nom: '',
    prenom: '',
    telephone: '',
    email: '',
    collineId: null,
    estCooperative: false
  })

  useEffect(() => {
    api.get('/api/provinces').then((r) => setProvinces(r.data)).catch(() => {})
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    setData(null)
    api.get('/api/agriculteurs', { params: { page, size: 50 } })
      .then((r) => setData(r.data))
      .catch((e) => setError(errorMessage(e)))
  }, [page])

  function search() {
    if (!telephone.trim()) return
    setData(null)
    api.get('/api/agriculteurs/recherche', { params: { telephone: telephone.trim() } })
      .then((r) => setData({ content: r.data, totalElements: r.data.length, totalPages: 1, number: 0 }))
      .catch((e) => setError(errorMessage(e)))
  }

  function resetList() {
    setTelephone('')
    setPage(0)
  }

  function onProvince(id) {
    setAll({ provinceId: id, zoneId: null, collineId: null })
    setZones([])
    setCollines([])
    if (id) api.get(`/api/provinces/${id}/zones`).then((r) => setZones(r.data)).catch(() => {})
  }

  function onZone(id) {
    setAll({ zoneId: id, collineId: null })
    setCollines([])
    if (id) api.get(`/api/zones/${id}/collines`).then((r) => setCollines(r.data)).catch(() => {})
  }

  async function notify(e) {
    e.preventDefault()
    setNotifyError('')
    try {
      await api.post(`/api/agriculteurs/${notifyFor.id}/notifier`, notifyForm)
      setMsg(`Email envoyé à ${notifyFor.email}`)
      setNotifyFor(null)
      setNotifyForm({ sujet: '', message: '' })
    } catch (err) {
      setNotifyError(errorMessage(err))
    }
  }

  async function create(e) {
    e.preventDefault()
    setMsg('')
    try {
      const payload = {
        numeroIdentite: form.numeroIdentite,
        nom: form.nom,
        prenom: form.prenom,
        telephone: form.telephone || undefined,
        email: form.email || undefined,
        collineId: Number(form.collineId),
        estCooperative: Boolean(form.estCooperative)
      }
      const { data: created } = await api.post('/api/agriculteurs', payload)
      setMsg(`${created.numeroIdentite} — ${created.nom} ${created.prenom} créé`)
      setShowCreate(false)
      reset()
      setPage(0)
    } catch (err) {
      setError(errorMessage(err))
    }
  }

  if (error) return <ErrorBox message={error} />
  if (!data) return <Loading />

  const list = data.content

  return (
    <>
      <SuccessBox message={msg} />
      <div className="row">
        <h1 style={{ margin: 0 }}>Agriculteurs</h1>
        <button className="btn" onClick={() => setShowCreate((v) => !v)}>
          {showCreate ? 'Annuler' : 'Nouvel agriculteur'}
        </button>
      </div>

      <div className="filter-bar">
        <input value={telephone} onChange={(e) => setTelephone(e.target.value)} placeholder="Rechercher par téléphone" style={{ width: 220 }} />
        <button className="btn outline" onClick={search}>Rechercher</button>
        <button className="btn outline" onClick={resetList}>Tout afficher</button>
      </div>

      {notifyFor && (
        <form className="card" onSubmit={notify}>
          <h2>Notifier {notifyFor.prenom} {notifyFor.nom} — {notifyFor.email}</h2>
          <ErrorBox message={notifyError} />
          <div className="form-grid">
            <Field label="Sujet">
              <input value={notifyForm.sujet} onChange={(e) => setNotifyForm((f) => ({ ...f, sujet: e.target.value }))} placeholder="Votre ticket FOMI" required />
            </Field>
            <Field label="Message">
              <textarea rows={5} value={notifyForm.message} onChange={(e) => setNotifyForm((f) => ({ ...f, message: e.target.value }))} placeholder="Bonjour, votre engrais est disponible au dépôt..." required />
            </Field>
          </div>
          <div className="row">
            <button className="btn">Envoyer l'email</button>
            <button type="button" className="btn outline" onClick={() => setNotifyFor(null)}>Annuler</button>
          </div>
        </form>
      )}

      {showCreate && (
        <form className="card" onSubmit={create}>
          <h2>Nouvel agriculteur</h2>
          <div className="form-grid">
            <Field label="Numéro d'identité">
              <input value={form.numeroIdentite} onChange={set('numeroIdentite')} placeholder="AGR-1001" required />
            </Field>
            <Field label="Nom">
              <input value={form.nom} onChange={set('nom')} required />
            </Field>
            <Field label="Prénom">
              <input value={form.prenom} onChange={set('prenom')} required />
            </Field>
            <Field label="Téléphone">
              <input value={form.telephone} onChange={set('telephone')} placeholder="79xxxxxxx" />
            </Field>
            <Field label="Email">
              <input type="email" value={form.email} onChange={set('email')} placeholder="agriculteur@example.bi" />
            </Field>
            <Field label="Province">
              <select value={form.provinceId || ''} onChange={(e) => onProvince(e.target.value)}>
                <option value="">—</option>
                {provinces.map((p) => <option key={p.id} value={p.id}>{p.nom}</option>)}
              </select>
            </Field>
            <Field label="Zone">
              <select value={form.zoneId || ''} onChange={(e) => onZone(e.target.value)}>
                <option value="">—</option>
                {zones.map((z) => <option key={z.id} value={z.id}>{z.nom}</option>)}
              </select>
            </Field>
            <Field label="Colline">
              <select value={form.collineId || ''} onChange={set('collineId')} required>
                <option value="">—</option>
                {collines.map((c) => <option key={c.id} value={c.id}>{c.nom}</option>)}
              </select>
            </Field>
            <label className="field" style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
              <input type="checkbox" checked={form.estCooperative} onChange={(e) => setAll({ estCooperative: e.target.checked })} style={{ width: 'auto' }} />
              <span>Coopérative</span>
            </label>
          </div>
          <button className="btn">Créer</button>
        </form>
      )}

      <div className="card">
        <table>
          <thead>
            <tr><th>Identité</th><th>Nom</th><th>Téléphone</th><th>Email</th><th>Colline</th><th>Type</th><th></th></tr>
          </thead>
          <tbody>
            {list.length === 0 && <tr><td colSpan={7}><Empty /></td></tr>}
            {list.map((a) => (
              <tr key={a.id}>
                <td><strong>{a.numeroIdentite}</strong></td>
                <td>{a.nom} {a.prenom}</td>
                <td>{a.telephone}</td>
                <td>{a.email || '—'}</td>
                <td>{a.collineNom}</td>
                <td>{a.estCooperative ? 'Coopérative' : 'Individuel'}</td>
                <td>
                  <button className="btn outline" disabled={!a.email} onClick={() => { setNotifyFor(a); setNotifyForm({ sujet: '', message: '' }); setNotifyError('') }}>
                    Notifier
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <p className="muted">{data.totalElements} agriculteur(s)</p>
        <Pagination page={data.number} totalPages={data.totalPages} onPage={setPage} />
      </div>
    </>
  )
}
