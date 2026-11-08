import { useEffect, useState } from 'react'
import { api, errorMessage } from '../api/client'
import { Loading, ErrorBox, SuccessBox, Badge, Field, useForm, Empty } from '../components/ui'

const ROLE_LABELS = {
  ADMIN: 'Admin',
  AGENT_ZONE: 'Agent zone',
  AGENT_COLLINE: 'Agent colline',
  SUPERVISEUR: 'Superviseur',
  AGENT_LOGISTIQUE: 'Agent logistique'
}

export default function Utilisateurs() {
  const [list, setList] = useState(null)
  const [depots, setDepots] = useState([])
  const [error, setError] = useState('')
  const [msg, setMsg] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, set, setAll, reset] = useForm({
    username: '',
    password: '',
    nomComplet: '',
    role: 'AGENT_COLLINE',
    depotId: null,
    actif: true
  })

  useEffect(() => {
    api.get('/api/utilisateurs').then((r) => setList(r.data)).catch((e) => setError(errorMessage(e)))
    api.get('/api/depots').then((r) => setDepots(r.data)).catch(() => {})
  }, [])

  function startCreate() {
    setEditing(null)
    setError('')
    setMsg('')
    reset()
    setShowForm(true)
  }

  function closeForm() {
    setShowForm(false)
    setEditing(null)
  }

  function startEdit(u) {
    setEditing(u)
    setAll({
      username: u.username,
      password: '',
      nomComplet: u.nomComplet,
      role: u.role,
      depotId: u.depotId,
      actif: u.actif
    })
    setShowForm(true)
  }

  async function submit(e) {
    e.preventDefault()
    setMsg('')
    setError('')
    try {
      const payload = {
        username: form.username,
        nomComplet: form.nomComplet,
        role: form.role,
        actif: form.actif
      }
      if (form.role === 'AGENT_COLLINE' && form.depotId) payload.depotId = Number(form.depotId)
      if (form.password) payload.password = form.password
      const { data } = editing
        ? await api.put(`/api/utilisateurs/${editing.id}`, payload)
        : await api.post('/api/utilisateurs', payload)
      setMsg(`Utilisateur ${data.username} ${editing ? 'modifié' : 'créé'}`)
      setShowForm(false)
      setEditing(null)
      api.get('/api/utilisateurs').then((r) => setList(r.data)).catch(() => {})
    } catch (err) {
      setError(errorMessage(err))
    }
  }

  if (!list) return error ? <ErrorBox message={error} /> : <Loading />

  return (
    <>
      <SuccessBox message={msg} />
      <ErrorBox message={error} />
      <div className="row page-actions">
        <div>
          <h2 className="section-title">Utilisateurs</h2>
          <p className="section-sub">Comptes, rôles et affectations aux dépôts.</p>
        </div>
        <button className="btn" onClick={() => (showForm ? closeForm() : startCreate())}>
          {showForm ? 'Annuler' : 'Nouvel utilisateur'}
        </button>
      </div>

      {showForm && (
        <form className="card" onSubmit={submit}>
          <h2>{editing ? `Modifier ${editing.username}` : 'Nouvel utilisateur'}</h2>
          <div className="form-grid">
            <Field label="Nom d'utilisateur">
              <input value={form.username} onChange={set('username')} required />
            </Field>
            <Field label={editing ? 'Nouveau mot de passe (optionnel)' : 'Mot de passe (min 6)'}>
              <input type="password" value={form.password} onChange={set('password')} minLength={6} required={!editing} />
            </Field>
            <Field label="Nom complet">
              <input value={form.nomComplet} onChange={set('nomComplet')} required />
            </Field>
            <Field label="Rôle">
              <select value={form.role} onChange={set('role')}>
                {Object.entries(ROLE_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
            </Field>
            {form.role === 'AGENT_COLLINE' && (
              <Field label="Dépôt affecté">
                <select value={form.depotId || ''} onChange={set('depotId')} required>
                  <option value="">—</option>
                  {depots.map((d) => <option key={d.id} value={d.id}>{d.nom} ({d.code})</option>)}
                </select>
              </Field>
            )}
            {editing && (
              <label className="field" style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
                <input type="checkbox" checked={form.actif} onChange={(e) => setAll({ actif: e.target.checked })} style={{ width: 'auto' }} />
                <span>Compte actif</span>
              </label>
            )}
          </div>
          <button className="btn">{editing ? 'Enregistrer' : 'Créer'}</button>
          <button type="button" className="btn outline" onClick={closeForm}>Annuler</button>
        </form>
      )}

      <div className="card">
        <table>
          <thead>
            <tr><th>Utilisateur</th><th>Nom</th><th>Rôle</th><th>Dépôt</th><th>Statut</th><th></th></tr>
          </thead>
          <tbody>
            {list.length === 0 && <tr><td colSpan={6}><Empty /></td></tr>}
            {list.map((u) => (
              <tr key={u.id}>
                <td><strong>{u.username}</strong></td>
                <td>{u.nomComplet}</td>
                <td><Badge tone="green">{ROLE_LABELS[u.role]}</Badge></td>
                <td>{u.depotId || '—'}</td>
                <td>{u.actif ? <Badge tone="green">Actif</Badge> : <Badge tone="red">Inactif</Badge>}</td>
                <td><button className="btn outline" onClick={() => startEdit(u)}>Modifier</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}
