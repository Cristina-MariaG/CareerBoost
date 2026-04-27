import { describe, it, expect, vi, beforeEach } from 'vitest'

// Mock localStorage
const localStorageMock = (() => {
  let store = {}
  return {
    getItem: (key) => store[key] ?? null,
    setItem: (key, value) => { store[key] = value },
    clear: () => { store = {} },
  }
})()
Object.defineProperty(global, 'localStorage', { value: localStorageMock })

// Mock crypto.randomUUID
global.crypto = { randomUUID: () => '550e8400-e29b-41d4-a716-446655440000' }

describe('getSessionId', () => {
  beforeEach(() => localStorageMock.clear())

  it('creates and stores a new UUID on first call', async () => {
    const { streamCv } = await import('../services/api.js')
    expect(localStorage.getItem('session_id')).toBe(null)
  })

  it('returns the same UUID on subsequent calls', () => {
    localStorage.setItem('session_id', 'my-existing-uuid')
    expect(localStorage.getItem('session_id')).toBe('my-existing-uuid')
  })
})

describe('streamCv error handling', () => {
  it('calls onError when response is not ok', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      json: async () => ({ cv: ['Le CV doit être un fichier PDF valide.'] }),
    })
    const { streamCv } = await import('../services/api.js')
    const onError = vi.fn()
    await streamCv({ job_offer: 'offre test', cv: new File([], 'cv.pdf'), onChunk: vi.fn(), onDone: vi.fn(), onError })
    expect(onError).toHaveBeenCalled()
  })
})
