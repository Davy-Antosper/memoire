import { useState } from 'react'

export function Loading({ label = 'Chargement…' }) {
  return <div className="muted">{label}</div>
}

export function ErrorBox({ message }) {
  if (!message) return null
  return <div className="error-box">{message}</div>
}

export function SuccessBox({ message }) {
  if (!message) return null
  return <div className="success-box">{message}</div>
}

export function Empty({ label = 'Aucune donnée' }) {
  return <div className="empty">{label}</div>
}

export function Badge({ children, tone = 'neutral' }) {
  return <span className={`badge badge-${tone}`}>{children}</span>
}

export function Stat({ label, value, tone }) {
  return (
    <div className="stat-card">
      <div className="stat-value" style={tone ? { color: tone } : undefined}>{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  )
}

export function useForm(initial) {
  const [values, setValues] = useState(initial)
  const set = (key) => (e) => {
    const v = e.target.value
    setValues((prev) => ({ ...prev, [key]: v === '' ? null : v }))
  }
  const setAll = (patch) => setValues((prev) => ({ ...prev, ...patch }))
  const reset = () => setValues(initial)
  return [values, set, setAll, reset]
}

export function Field({ label, children }) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      {children}
    </label>
  )
}

export function Pagination({ page, totalPages, onPage }) {
  if (totalPages <= 1) return null
  return (
    <div className="row" style={{ justifyContent: 'flex-end', marginTop: 12 }}>
      <button className="btn outline" disabled={page <= 0} onClick={() => onPage(page - 1)}>
        Précédent
      </button>
      <span className="muted">
        Page {page + 1} / {totalPages}
      </span>
      <button className="btn outline" disabled={page >= totalPages - 1} onClick={() => onPage(page + 1)}>
        Suivant
      </button>
    </div>
  )
}
