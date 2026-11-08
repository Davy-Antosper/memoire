import { useEffect, useState } from 'react'
import { api, errorMessage } from '../api/client'
import { Loading, ErrorBox, Stat, Empty } from '../components/ui'
import { AlertIcon, DistributionIcon, PackageIcon, TrendIcon, WarningIcon } from '../components/icons'

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      api.get('/api/statistiques/ruptures'),
      api.get('/api/statistiques/stocks-par-province'),
      api.get('/api/statistiques/taux-service'),
      api.get('/api/alertes', { params: { nonTraitees: true } })
    ])
      .then(([ruptures, stocks, taux, alertes]) => {
        setData({ ruptures: ruptures.data, stocks: stocks.data, taux: taux.data, alertes: alertes.data })
      })
      .catch((e) => setError(errorMessage(e)))
  }, [])

  if (error) return <ErrorBox message={error} />
  if (!data) return <Loading />

  const totalStock = data.stocks.reduce((s, r) => s + r.stock, 0)
  const totalDistribue = data.stocks.reduce((s, r) => s + r.distribue, 0)
  const servis = data.taux.reduce((s, r) => s + r.servi, 0)
  const commandes = data.taux.reduce((s, r) => s + r.commande, 0)

  const tauxService = commandes ? Math.round((servis / commandes) * 100) : null

  return (
    <>
      <div className="page-actions">
        <div>
          <h2 className="section-title">Vue d’ensemble</h2>
          <p className="section-sub">Indicateurs consolidés du réseau de stockage FOMI.</p>
        </div>
      </div>
      <div className="stat-grid">
        <Stat icon={PackageIcon} label="Stock total (sacs)" value={totalStock.toLocaleString('fr-FR')} hint="Tous dépôts confondus" />
        <Stat icon={DistributionIcon} label="Distribué (sacs)" value={totalDistribue.toLocaleString('fr-FR')} hint="Cumul des sorties" />
        <Stat
          icon={WarningIcon}
          label="Ruptures"
          value={data.ruptures.length}
          tone={data.ruptures.length ? 'var(--red)' : undefined}
          hint={data.ruptures.length ? 'Action requise' : 'Aucune rupture'}
        />
        <Stat
          icon={AlertIcon}
          label="Alertes non traitées"
          value={data.alertes.length}
          tone={data.alertes.length ? 'var(--amber)' : undefined}
          hint={data.alertes.length ? 'À examiner' : 'Tout est traité'}
        />
        <Stat
          icon={TrendIcon}
          label="Taux de service"
          value={tauxService === null ? '—' : `${tauxService}%`}
          tone={tauxService !== null && tauxService < 80 ? 'var(--amber)' : undefined}
          hint="Servi / commandé"
        />
      </div>

      <div className="card">
        <h2>Ruptures de stock</h2>
        {data.ruptures.length === 0 ? (
          <Empty label="Aucune rupture" />
        ) : (
          <table>
            <thead>
              <tr><th>Dépôt</th><th>Engrais</th></tr>
            </thead>
            <tbody>
              {data.ruptures.map((r, i) => (
                <tr key={i}>
                  <td>{r.depotNom} ({r.depotCode})</td>
                  <td>{r.engraisNom}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="card">
        <h2>Stocks par province</h2>
        {data.stocks.length === 0 ? (
          <Empty />
        ) : (
          <table>
            <thead>
              <tr>
                <th>Province</th>
                <th className="num">Stock</th>
                <th className="num">Distribué</th>
                <th className="num">Reste</th>
              </tr>
            </thead>
            <tbody>
              {data.stocks.map((r, i) => (
                <tr key={i}>
                  <td>{r.nom}</td>
                  <td className="num">{r.stock}</td>
                  <td className="num">{r.distribue}</td>
                  <td className="num">{r.reste}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  )
}
