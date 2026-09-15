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
  const [form, set, setAll, reset] = useForm({
    numeroIdentite: '',
    nom: '',
    prenom: '',
    telephone: '',
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

  async function create(e) {
    e.preventDefault()
    setMsg('')
    try {
      const payload = {
        numeroIdentite: form.numeroIdentite,
        nom: form.nom,
        prenom: form.prenom,
        telephone: form.telephone || undefined,
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
            <tr><th>Identité</th><th>Nom</th><th>Téléphone</th><th>Colline</th><th>Type</th></tr>
          </thead>
          <tbody>
            {list.length === 0 && <tr><td colSpan={5}><Empty /></td></tr>}
            {list.map((a) => (
              <tr key={a.id}>
                <td><strong>{a.numeroIdentite}</strong></td>
                <td>{a.nom} {a.prenom}</td>
                <td>{a.telephone}</td>
                <td>{a.collineNom}</td>
                <td>{a.estCooperative ? 'Coopérative' : 'Individuel'}</td>
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
