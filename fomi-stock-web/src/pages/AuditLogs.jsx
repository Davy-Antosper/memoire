import { useEffect, useState } from 'react'
import { api, errorMessage } from '../api/client'
import { Loading, ErrorBox, Badge, Empty, Pagination } from '../components/ui'

const ACTION_TONES = {
  AUTH_LOGIN: 'blue',
  AUTH_LOGOUT: 'neutral',
  TICKET_CREATE: 'green',
  TICKET_UPDATE: 'amber',
  TICKET_ACTIVATE: 'green',
  TICKET_REJECT: 'red',
  LOT_CREATE: 'green',
  DISTRIBUTION: 'blue',
  RECEPTION: 'green',
  TRANSFERT: 'amber',
  ALERTE_CREATE: 'amber',
  ALERTE_RESOLVE: 'green'
}

function ToneBadge({ action }) {
  return <Badge tone={ACTION_TONES[action] || 'neutral'}>{action}</Badge>
}

export default function AuditLogs() {
  const [data, setData] = useState(null)
  const [action, setAction] = useState('')
  const [entityType, setEntityType] = useState('')
  const [page, setPage] = useState(0)
  const [error, setError] = useState('')

  useEffect(() => {
    setData(null)
    api.get('/api/audit-logs', {
      params: {
        ...(action ? { action } : {}),
        ...(entityType ? { entityType } : {}),
        page,
        size: 50
      }
    })
      .then((r) => setData(r.data))
      .catch((e) => setError(errorMessage(e)))
  }, [action, entityType, page])

  if (error) return <ErrorBox message={error} />
  if (!data) return <Loading />

  return (
    <>
      <h1>Logs d’audit</h1>

      <div className="filter-bar">
        <input
          placeholder="Action (ex : TICKET_ACTIVATE)"
          value={action}
          onChange={(e) => { setAction(e.target.value); setPage(0) }}
        />
        <input
          placeholder="Type d’entité (ex : TICKET)"
          value={entityType}
          onChange={(e) => { setEntityType(e.target.value); setPage(0) }}
        />
        <span className="muted">{data.totalElements} entrée(s)</span>
      </div>

      <div className="card">
        {data.content.length === 0 ? (
          <Empty />
        ) : (
          <table>
            <thead>
              <tr>
                <th>Date</th><th>Utilisateur</th><th>Action</th><th>Entité</th><th className="num">Id</th><th>Détails</th>
              </tr>
            </thead>
            <tbody>
              {data.content.map((l) => (
                <tr key={l.id}>
                  <td>{new Date(l.createdAt).toLocaleString('fr-FR')}</td>
                  <td>{l.utilisateurUsername}</td>
                  <td><ToneBadge action={l.action} /></td>
                  <td>{l.entityType}</td>
                  <td className="num">{l.entityId ?? '—'}</td>
                  <td style={{ maxWidth: 380, whiteSpace: 'pre-wrap', wordBreak: 'break-word', fontSize: 12 }}>
                    {l.detailsJson || '—'}
                  </td>
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
