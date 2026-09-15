import { useEffect, useState } from 'react'
import { api, errorMessage } from '../api/client'
import { Loading, ErrorBox, Badge, Empty } from '../components/ui'

const NIVEAU_TONES = { CRITIQUE: 'red', HAUTE: 'red', MOYENNE: 'amber', BASSE: 'neutral' }

export default function Alertes() {
  const [list, setList] = useState(null)
  const [error, setError] = useState('')
  const [nonTraitees, setNonTraitees] = useState(true)

  function load(onlyUntreated) {
    setList(null)
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

  if (error) return <ErrorBox message={error} />
  if (!list) return <Loading />

  return (
    <>
      <h1>Alertes</h1>
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
                    ) : (
                      <button className="btn outline" onClick={() => traiter(a.id)}>Traiter</button>
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
