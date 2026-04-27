import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

export default api

function getSessionId() {
  let id = localStorage.getItem('session_id')
  if (!id) {
    id = crypto.randomUUID()
    localStorage.setItem('session_id', id)
  }
  return id
}

export async function streamCv({ job_offer, cv, cover_letter, mode = 'adapt', onChunk, onDone, onError }) {
  const formData = new FormData()
  formData.append('job_offer', job_offer)
  formData.append('session_id', getSessionId())
  formData.append('cv', cv)
  formData.append('mode', mode)
  if (cover_letter) formData.append('cover_letter', cover_letter)

  const response = await fetch('/api/agents/cv/', {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    const err = await response.json()
    onError(err)
    return
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let finished = false

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    const lines = decoder.decode(value).split('\n')
    for (const line of lines) {
      if (!line.startsWith('data: ')) continue
      const payload = line.slice(6)
      if (payload === '[DONE]') { finished = true; onDone(); return }
      try {
        const { text, error } = JSON.parse(payload)
        if (error) { finished = true; onError(error); return }
        if (text) onChunk(text)
      } catch {}
    }
  }

  if (!finished) onError('La connexion a été interrompue. Réessaie.')
}

export async function getHistory() {
  const sessionId = getSessionId()
  const response = await api.get(`/history/?session_id=${sessionId}`)
  return response.data
}

export async function streamLinkedIn({ description, tone, onChunk, onDone, onError }) {
  const response = await fetch('/api/agents/linkedin/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ description, tone, session_id: getSessionId() }),
  })

  if (!response.ok) {
    const err = await response.json()
    onError(err)
    return
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let finished = false

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    const lines = decoder.decode(value).split('\n')
    for (const line of lines) {
      if (!line.startsWith('data: ')) continue
      const payload = line.slice(6)
      if (payload === '[DONE]') { finished = true; onDone(); return }
      try {
        const { text, error } = JSON.parse(payload)
        if (error) { finished = true; onError(error); return }
        if (text) onChunk(text)
      } catch {}
    }
  }

  if (!finished) onError('La connexion a été interrompue. Réessaie.')
}
