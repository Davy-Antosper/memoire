import { useEffect, useState } from 'react'
import { api, errorMessage } from '../api/client'
import { Loading, ErrorBox, Badge, Empty } from '../components/ui'
import { useAuth } from '../auth/AuthContext'

const NIVEAU_TONES = { INFO: 'blue', WARNING: 'amber', CRITICAL: 'red' }

export default function Alertes() {
  const { user } = useAuth()
  const canTraiter = user.role === 'ADMIN'
  const [list, setList] = useState(null)
  const [error, setError] = useState('')
  const [nonTraitees, setNonTraitees] = useState(true)

  function load(onlyUntreated) {
    setList(null)
    setError('')
    api.get('/api/alertes', { params: onlyUntreated ? { nonTraitees: true } : {} })
      .then((r) => setList(r.data))
      .catch((e) => setError(errorMessage(e)))
  }

  useEffect(() => {
    load(nonTraitees)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  function traiter(id) {
    api.patch(`/api/alertes/${id}/traiter`)
      .then(() => load(nonTraitees))
      .catch((e) => setError(errorMessage(e)))
  }

  if (!list) return error ? <ErrorBox message={error} /> : <Loading />

  return (
    <>
      <div className="page-actions">
        <div>
          <h2 className="section-title">Alertes de stock</h2>
          <p className="section-sub">Seuils bas, ruptures et anomalies détectées sur les dépôts.</p>
        </div>
      </div>
      <ErrorBox message={error} />
      <div className="filter-bar">
        <label style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <input type="checkbox" checked={nonTraitees} onChange={(e) => {
            setNonTraitees(e.target.checked)
            load(e.target.checked)
          }} style={{ width: 'auto' }} />
          Non traitées uniquement
        </label>
      </div>

      <div className="card">
        {list.length === 0 ? (
          <Empty label="Aucune alerte" />
        ) : (
          <table>
            <thead>
              <tr><th>Dépôt</th><th>Engrais</th><th>Type</th><th>Niveau</th><th>Message</th><th>Date</th><th></th></tr>
            </thead>
            <tbody>
              {list.map((a) => (
                <tr key={a.id}>
                  <td>{a.depotNom} ({a.depotCode})</td>
                  <td>{a.engraisTypeCode}</td>
                  <td>{a.type}</td>
                  <td><Badge tone={NIVEAU_TONES[a.niveau] || 'neutral'}>{a.niveau}</Badge></td>
                  <td>{a.message}</td>
                  <td>{new Date(a.createdAt).toLocaleString('fr-FR')}</td>
                  <td>
                    {a.traitee ? (
                      <Badge tone="green">Traitée</Badge>
                    ) : canTraiter ? (
                      <button className="btn outline" onClick={() => traiter(a.id)}>Traiter</button>
                    ) : (
                      <Badge tone="amber">Non traitée</Badge>
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
