import { useEffect, useState } from 'react'
import { api, errorMessage } from '../api/client'
import { Loading, ErrorBox, SuccessBox, Badge, Empty, Field, useForm } from '../components/ui'
import { useAuth } from '../auth/AuthContext'

const NIVEAU_TONES = { PROVINCE: 'green', ZONE: 'amber' }

const EMPTY_FORM = {
  code: '',
  nom: '',
  niveau: 'PROVINCE',
  provinceId: null,
  communeId: null,
  zoneId: null,
  seuilAlerteMin: 10
}

export default function Depots() {
  const { user } = useAuth()
  const [depots, setDepots] = useState(null)
  const [error, setError] = useState('')
  const [selected, setSelected] = useState(null)
  const [stock, setStock] = useState(null)
  const [showCreate, setShowCreate] = useState(false)
  const [editing, setEditing] = useState(null)
  const [provinces, setProvinces] = useState([])
  const [communes, setCommunes] = useState([])
  const [zones, setZones] = useState([])
  const [msg, setMsg] = useState('')
  const [form, set, setAll] = useForm(EMPTY_FORM)

  // Seuils d'alerte par produit : le seuil du dépôt n'est qu'un repli.
  const [engraisTypes, setEngraisTypes] = useState([])
  const [seuils, setSeuils] = useState([])
  const [seuilDraft, setSeuilDraft] = useState({})
  const [seuilSaving, setSeuilSaving] = useState(null)
  const [seuilMsg, setSeuilMsg] = useState('')
  const [seuilError, setSeuilError] = useState('')

  useEffect(() => {
    api.get('/api/depots')
      .then((r) => setDepots(r.data))
      .catch((e) => setError(errorMessage(e)))
    api.get('/api/engrais-types')
      .then((r) => setEngraisTypes(r.data))
      .catch(() => {})
  }, [])

  useEffect(() => {
    if (!showCreate) return
    setCommunes([])
    setZones([])
    api.get('/api/provinces').then((r) => setProvinces(r.data)).catch(() => {})
    if (editing?.provinceId) {
      api.get(`/api/provinces/${editing.provinceId}/communes`)
        .then((r) => setCommunes(r.data))
        .catch(() => {})
    }
    if (editing?.communeId) {
      api.get(`/api/communes/${editing.communeId}/zones`)
        .then((r) => setZones(r.data))
        .catch(() => {})
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [showCreate])

  function onProvince(id) {
    setAll({ provinceId: id, communeId: null, zoneId: null })
    setCommunes([])
    setZones([])
    if (id) api.get(`/api/provinces/${id}/communes`).then((r) => setCommunes(r.data)).catch(() => {})
  }

  function onCommune(id) {
    setAll({ communeId: id, zoneId: null })
    setZones([])
    if (id) api.get(`/api/communes/${id}/zones`).then((r) => setZones(r.data)).catch(() => {})
  }

  function openDepot(depot) {
    setSelected(depot)
    setStock(null)
    setSeuils([])
    setSeuilDraft({})
    setSeuilMsg('')
    setSeuilError('')
    api.get(`/api/depots/${depot.id}/stock`)
      .then((r) => setStock(r.data))
      .catch((e) => setError(errorMessage(e)))
    chargerSeuils(depot.id)
  }

  function chargerSeuils(depotId) {
    api.get('/api/seuils-alerte', { params: { depotId } })
      .then((r) => {
        setSeuils(r.data)
        setSeuilDraft(Object.fromEntries(r.data.map((s) => [s.engraisTypeId, s.seuilMin])))
      })
      .catch((e) => setSeuilError(errorMessage(e)))
  }

  async function enregistrerSeuil(engraisTypeId) {
    const depot = selected
    if (!depot) return
    const valeur = Number(seuilDraft[engraisTypeId])
    if (!Number.isFinite(valeur) || valeur < 0) {
      setSeuilError("Le seuil doit être un nombre positif (en sacs de 25 kg).")
      return
    }
    const existant = seuils.find((s) => s.engraisTypeId === engraisTypeId)
    setSeuilSaving(engraisTypeId)
    setSeuilError('')
    setSeuilMsg('')
    try {
      const payload = {
        depotId: depot.id,
        engraisTypeId,
        seuilMin: valeur,
        criticite: existant?.criticite || 'WARNING'
      }
      const { data } = existant
        ? await api.put(`/api/seuils-alerte/${existant.id}`, payload)
        : await api.post('/api/seuils-alerte', payload)
      setSeuils((prev) => {
        const autres = prev.filter((s) => s.engraisTypeId !== engraisTypeId)
        return [...autres, data].sort((a, b) => a.engraisTypeCode.localeCompare(b.engraisTypeCode))
      })
      setSeuilDraft((prev) => ({ ...prev, [engraisTypeId]: data.seuilMin }))
      setSeuilMsg(`Seuil du produit mis à jour : ${valeur} sacs`)
      // Le tableau de stock affiche le seuil effectif : on le recharge.
      api.get(`/api/depots/${depot.id}/stock`)
        .then((r) => setStock(r.data))
        .catch(() => {})
    } catch (err) {
      setSeuilError(errorMessage(err))
    } finally {
      setSeuilSaving(null)
    }
  }

  async function supprimerSeuil(seuil) {
    if (!window.confirm(`Retirer le seuil propre à ${seuil.engraisTypeCode} ? Le dépôt appliquera de nouveau son seuil par défaut (${selected.seuilAlerteMin} sacs).`)) {
      return
    }
    setSeuilSaving(seuil.engraisTypeId)
    setSeuilError('')
    setSeuilMsg('')
    try {
      await api.delete(`/api/seuils-alerte/${seuil.id}`)
      setSeuils((prev) => prev.filter((s) => s.id !== seuil.id))
      setSeuilDraft((prev) => {
        const copie = { ...prev }
        delete copie[seuil.engraisTypeId]
        return copie
      })
      setSeuilMsg(`Seuil propre à ${seuil.engraisTypeCode} retiré`)
      api.get(`/api/depots/${selected.id}/stock`)
        .then((r) => setStock(r.data))
        .catch(() => {})
    } catch (err) {
      setSeuilError(errorMessage(err))
    } finally {
      setSeuilSaving(null)
    }
  }

  function closeForm() {
    setShowCreate(false)
    setEditing(null)
    setMsg('')
  }

  function startCreate() {
    setEditing(null)
    setError('')
    setMsg('')
    setAll(EMPTY_FORM)
    setShowCreate(true)
  }

  function startEdit(d) {
    setEditing(d)
    setError('')
    setMsg('')
    setAll({
      code: d.code,
      nom: d.nom,
      niveau: d.niveau,
      provinceId: d.provinceId,
      communeId: d.communeId,
      zoneId: d.zoneId,
      seuilAlerteMin: d.seuilAlerteMin
    })
    setShowCreate(true)
  }

  async function save(e) {
    e.preventDefault()
    setMsg('')
    setError('')
    try {
      const payload = {
        code: form.code,
        nom: form.nom,
        niveau: form.niveau,
        provinceId: form.niveau === 'PROVINCE' && form.provinceId ? Number(form.provinceId) : null,
        zoneId: form.niveau === 'ZONE' && form.zoneId ? Number(form.zoneId) : null,
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
      closeForm()
    } catch (err) {
      setError(errorMessage(err))
    }
  }

  if (!depots) return error ? <ErrorBox message={error} /> : <Loading />

  return (
    <>
      <SuccessBox message={msg} />
      <ErrorBox message={error} />
      <div className="row page-actions">
        <div>
          <h2 className="section-title">Dépôts</h2>
          <p className="section-sub">Réseau FOMI : dépôts provinciaux (logistique) et dépôts de zone (distribution).</p>
        </div>
        {user.role === 'ADMIN' && (
          <button className="btn outline" onClick={() => (showCreate ? closeForm() : startCreate())}>
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
                <option value="PROVINCE">Province (logistique)</option>
                <option value="ZONE">Zone (distribution)</option>
              </select>
            </Field>
            <Field label="Seuil d'alerte (sacs)">
              <input type="number" min="0" value={form.seuilAlerteMin} onChange={set('seuilAlerteMin')} />
            </Field>
            <Field label="Province">
              <select value={form.provinceId || ''} onChange={(e) => onProvince(e.target.value)} required={form.niveau === 'PROVINCE'}>
                <option value="">—</option>
                {provinces.map((p) => <option key={p.id} value={p.id}>{p.nom}</option>)}
              </select>
            </Field>
            {form.niveau === 'ZONE' && (
              <>
                <Field label="Commune">
                  <select value={form.communeId || ''} onChange={(e) => onCommune(e.target.value)} required>
                    <option value="">—</option>
                    {communes.map((c) => <option key={c.id} value={c.id}>{c.nom}</option>)}
                  </select>
                </Field>
                <Field label="Zone">
                  <select value={form.zoneId || ''} onChange={set('zoneId')} required disabled={!form.communeId}>
                    <option value="">—</option>
                    {zones.map((z) => <option key={z.id} value={z.id}>{z.nom}</option>)}
                  </select>
                </Field>
              </>
            )}
          </div>
          <div className="row" style={{ marginTop: 12 }}>
            <button className="btn">{editing ? 'Enregistrer' : 'Créer le dépôt'}</button>
            <button type="button" className="btn outline" onClick={closeForm}>Annuler</button>
          </div>
        </form>
      )}

      <div className="card">
        <table>
          <thead>
            <tr><th>Code</th><th>Nom</th><th>Niveau</th><th>Province</th><th>Commune</th><th>Zone</th><th></th></tr>
          </thead>
          <tbody>
            {depots.length === 0 && <tr><td colSpan={7}><Empty /></td></tr>}
            {depots.map((d) => (
              <tr key={d.id}>
                <td><strong>{d.code}</strong></td>
                <td>{d.nom}</td>
                <td><Badge tone={NIVEAU_TONES[d.niveau]}>{d.niveau}</Badge></td>
                <td>{d.provinceNom || '—'}</td>
                <td>{d.communeNom || '—'}</td>
                <td>{d.zoneNom || '—'}</td>
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

      {selected && (
        <div className="card">
          <h2>Seuils d'alerte par produit — {selected.code}</h2>
          <p className="section-sub">
            Un seuil propre à chaque engrais, en sacs de 25 kg. En l'absence de seuil
            spécifique, le dépôt applique son seuil par défaut ({selected.seuilAlerteMin} sacs).
          </p>
          <SuccessBox message={seuilMsg} />
          <ErrorBox message={seuilError} />
          <table>
            <thead>
              <tr>
                <th>Engrais</th>
                <th className="num">Seuil appliqué</th>
                <th>Origine</th>
                <th className="num">Nouveau seuil (sacs)</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {engraisTypes.length === 0 && <tr><td colSpan={5}><Empty /></td></tr>}
              {engraisTypes.map((e) => {
                const propre = seuils.find((s) => s.engraisTypeId === e.id)
                const applique = propre ? propre.seuilMin : selected.seuilAlerteMin
                const busy = seuilSaving === e.id
                const canEditSeuil = user.role === 'ADMIN'
                return (
                  <tr key={e.id}>
                    <td>
                      <strong>{e.code}</strong>
                      <div className="section-sub" style={{ margin: 0 }}>{e.nom}</div>
                    </td>
                    <td className="num">{applique}</td>
                    <td>
                      {propre
                        ? <Badge tone="amber">Propre au produit</Badge>
                        : <Badge tone="neutral">Défaut du dépôt</Badge>}
                    </td>
                    <td className="num">
                      <input
                        type="number"
                        min="0"
                        style={{ width: 90 }}
                        value={seuilDraft[e.id] ?? ''}
                        placeholder={String(applique)}
                        disabled={busy || !canEditSeuil}
                        onChange={(ev) => setSeuilDraft((prev) => ({ ...prev, [e.id]: ev.target.value }))}
                      />
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: 6 }}>
                        {canEditSeuil ? (
                          <>
                            <button
                              className="btn outline"
                              disabled={busy || seuilDraft[e.id] === undefined || seuilDraft[e.id] === ''}
                              onClick={() => enregistrerSeuil(e.id)}
                            >
                              {propre ? 'Modifier' : 'Définir'}
                            </button>
                            {propre && (
                              <button className="btn danger" disabled={busy} onClick={() => supprimerSeuil(propre)}>
                                Retirer
                              </button>
                            )}
                          </>
                        ) : (
                          <span className="section-sub" style={{ margin: 0 }}>Lecture seule</span>
                        )}
                      </div>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </>
  )
}
