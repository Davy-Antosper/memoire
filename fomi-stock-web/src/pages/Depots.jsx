import { useEffect, useState } from 'react'
import { api, errorMessage } from '../api/client'
import { Loading, ErrorBox, SuccessBox, Badge, Empty, Field, useForm } from '../components/ui'
import { useAuth } from '../auth/AuthContext'

const NIVEAU_TONES = { PROVINCE: 'green', ZONE: 'amber', COLLINE: 'neutral' }

export default function Depots() {
  const { user } = useAuth()
  const [depots, setDepots] = useState(null)
  const [error, setError] = useState('')
  const [selected, setSelected] = useState(null)
  const [stock, setStock] = useState(null)
  const [showCreate, setShowCreate] = useState(false)
  const [editing, setEditing] = useState(null)
  const [provinces, setProvinces] = useState([])
  const [zones, setZones] = useState([])
  const [collines, setCollines] = useState([])
  const [msg, setMsg] = useState('')
  const [form, set, setAll] = useForm({ code: '', nom: '', niveau: 'PROVINCE', provinceId: null, zoneId: null, collineId: null, seuilAlerteMin: 10 })

  useEffect(() => {
    api.get('/api/depots')
      .then((r) => setDepots(r.data))
      .catch((e) => setError(errorMessage(e)))
  }, [])

  useEffect(() => {
    if (!showCreate) return
    setProvinces([])
    setZones([])
    setCollines([])
    api.get('/api/provinces').then((r) => setProvinces(r.data)).catch(() => {})
    if (editing) {
      if (editing.provinceId) api.get(`/api/provinces/${editing.provinceId}/zones`).then((r) => setZones(r.data)).catch(() => {})
      if (editing.zoneId) api.get(`/api/zones/${editing.zoneId}/collines`).then((r) => setCollines(r.data)).catch(() => {})
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [showCreate])

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

  function openDepot(depot) {
    setSelected(depot)
    setStock(null)
    api.get(`/api/depots/${depot.id}/stock`)
      .then((r) => setStock(r.data))
      .catch((e) => setError(errorMessage(e)))
  }

  function startCreate() {
    setEditing(null)
    setAll({ code: '', nom: '', niveau: 'PROVINCE', provinceId: null, zoneId: null, collineId: null, seuilAlerteMin: 10 })
    setShowCreate(true)
  }

  function startEdit(d) {
    setEditing(d)
    setAll({
      code: d.code,
      nom: d.nom,
      niveau: d.niveau,
      provinceId: d.provinceId,
      zoneId: d.zoneId,
      collineId: d.collineId,
      seuilAlerteMin: d.seuilAlerteMin
    })
    setShowCreate(true)
  }

  async function save(e) {
    e.preventDefault()
    setMsg('')
    try {
      const payload = {
        code: form.code,
        nom: form.nom,
        niveau: form.niveau,
        provinceId: form.provinceId,
        zoneId: form.zoneId,
        collineId: form.collineId,
        seuilAlerteMin: Number(form.seuilAlerteMin)
      }
      const { data } = editing
        ? await api.put(`/api/depots/${editing.id}`, payload)
        : await api.post('/api/depots', payload)
      if (editing) {
        setDepots((prev) => prev.map((d) => (d.id === data.id ? data : d)))
      } else {
        setDepots((prev) => [...prev, data])
      }
      setMsg(editing ? 'Dépôt modifié' : 'Dépôt créé')
      setShowCreate(false)
      setEditing(null)
    } catch (err) {
      setError(errorMessage(err))
    }
  }

  if (error) return <ErrorBox message={error} />
  if (!depots) return <Loading />

  return (
    <>
      <SuccessBox message={msg} />
      <div className="row">
        <h1 style={{ margin: 0 }}>Dépôts</h1>
        {user.role === 'ADMIN' && (
          <button className="btn outline" onClick={startCreate}>
            {showCreate ? 'Annuler' : 'Nouveau dépôt'}
          </button>
        )}
      </div>

      {showCreate && (
        <form className="card" onSubmit={save}>
          <h2>{editing ? `Modifier ${editing.code}` : 'Nouveau dépôt'}</h2>
          <div className="form-grid">
            <Field label="Code">
              <input value={form.code} onChange={set('code')} placeholder="DEP-GIT-P" required />
            </Field>
            <Field label="Nom">
              <input value={form.nom} onChange={set('nom')} placeholder="Dépôt Gitega Province" required />
            </Field>
            <Field label="Niveau">
              <select value={form.niveau} onChange={set('niveau')}>
                <option value="PROVINCE">Province</option>
                <option value="ZONE">Zone</option>
                <option value="COLLINE">Colline</option>
              </select>
            </Field>
            <Field label="Seuil d'alerte (sacs)">
              <input type="number" min="0" value={form.seuilAlerteMin} onChange={set('seuilAlerteMin')} />
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
              <select value={form.collineId || ''} onChange={set('collineId')}>
                <option value="">—</option>
                {collines.map((c) => <option key={c.id} value={c.id}>{c.nom}</option>)}
              </select>
            </Field>
          </div>
          <button className="btn">{editing ? 'Enregistrer' : 'Créer le dépôt'}</button>
        </form>
      )}

      <div className="card">
        <table>
          <thead>
            <tr><th>Code</th><th>Nom</th><th>Niveau</th><th>Province</th><th></th></tr>
          </thead>
          <tbody>
            {depots.length === 0 && <tr><td colSpan={5}><Empty /></td></tr>}
            {depots.map((d) => (
              <tr key={d.id}>
                <td><strong>{d.code}</strong></td>
                <td>{d.nom}</td>
                <td><Badge tone={NIVEAU_TONES[d.niveau]}>{d.niveau}</Badge></td>
                <td>{d.provinceNom}</td>
                <td>
                  <div style={{ display: 'flex', gap: 6 }}>
                    <button className="btn outline" onClick={() => openDepot(d)}>Stock</button>
                    {user.role === 'ADMIN' && (
                      <button className="btn outline" onClick={() => startEdit(d)}>Modifier</button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selected && (
        <div className="card">
          <h2>Stock — {selected.nom} ({selected.code})</h2>
          {!stock ? (
            <Loading />
          ) : stock.length === 0 ? (
            <Empty label="Aucun stock pour ce dépôt" />
          ) : (
            <table>
              <thead>
                <tr><th>Engrais</th><th className="num">Disponible</th><th className="num">Seuil</th><th>État</th></tr>
              </thead>
              <tbody>
                {stock.map((s) => (
                  <tr key={s.engraisCode}>
                    <td>{s.engraisNom}</td>
                    <td className="num">{s.quantiteDisponible}</td>
                    <td className="num">{s.seuilAlerteMin}</td>
                    <td>
                      {s.quantiteDisponible === 0 ? (
                        <Badge tone="red">Rupture</Badge>
                      ) : s.quantiteDisponible <= s.seuilAlerteMin ? (
                        <Badge tone="amber">Bas</Badge>
                      ) : (
                        <Badge tone="green">OK</Badge>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </>
  )
}
