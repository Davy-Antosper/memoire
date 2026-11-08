import axios from 'axios'

const PROD_URL = 'https://fomi-stock-api-production.up.railway.app'

// En développement, on passe par le proxy Vite (origine identique) pour éviter
// les problèmes de CORS. En production, l'URL de l'API est utilisée directement.
const BASE_URL =
  import.meta.env.VITE_API_URL || (import.meta.env.DEV ? '' : PROD_URL)

export const api = axios.create({ baseURL: BASE_URL })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('fomi_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const url = err.config?.url || ''
    if (err.response?.status === 401 && !url.includes('/login')) {
      localStorage.removeItem('fomi_token')
      localStorage.removeItem('fomi_user')
      // L'état React est synchronisé par AuthContext via cet événement.
      window.dispatchEvent(new Event('fomi:unauthorized'))
    }
    return Promise.reject(err)
  }
)

export async function downloadCsv(url, params, filename) {
  const { data } = await api.get(url, { params, responseType: 'blob' })
  const blobUrl = URL.createObjectURL(data)
  const a = document.createElement('a')
  a.href = blobUrl
  a.download = filename
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(blobUrl)
}

export function errorMessage(err) {
  const data = err?.response?.data
  if (typeof data === 'string' && data.trim()) return data
  if (data?.erreur) return data.erreur
  if (data?.message) return data.message
  if (data?.error) return data.error
  if (Array.isArray(data?.errors)) {
    return data.errors.map((e) => e.message || e).join(', ')
  }
  if (data?.errors && typeof data.errors === 'object') {
    return Object.entries(data.errors)
      .map(([field, message]) => `${field} : ${message}`)
      .join(', ')
  }
  if (err?.code === 'ERR_NETWORK') {
    return 'Impossible de joindre le serveur. Vérifiez que l’API est démarrée.'
  }
  return err?.message || 'Erreur inattendue'
}
