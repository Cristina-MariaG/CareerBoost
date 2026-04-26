<template>
  <div v-if="props.content || streaming" class="result-card">
    <div class="result-card__sections" :class="{ 'result-card__sections--two-col': lmContent }">
      <div class="result-card__section">
        <div class="result-card__header">
          <span class="result-card__label">CV adapté</span>
          <div v-if="cvContent" class="result-card__actions">
            <button class="result-card__copy" @click="copy(cvContent, 'cv')">
              {{ copiedKey === 'cv' ? 'Copié !' : 'Copier' }}
            </button>
            <button class="result-card__download" @click="download(cvContent, 'cv-adapte')">
              Télécharger
            </button>
          </div>
        </div>
        <div class="result-card__body" v-html="renderMd(cvContent)"></div>
        <div v-if="streaming && !lmContent" class="result-card__cursor">▌</div>
      </div>

      <div v-if="lmContent" class="result-card__section">
        <div class="result-card__header">
          <span class="result-card__label">Lettre de motivation</span>
          <div class="result-card__actions">
            <button class="result-card__copy" @click="copy(lmContent, 'lm')">
              {{ copiedKey === 'lm' ? 'Copié !' : 'Copier' }}
            </button>
            <button class="result-card__download" @click="download(lmContent, 'lettre-motivation')">
              Télécharger
            </button>
          </div>
        </div>
        <div class="result-card__body" v-html="renderMd(lmContent)"></div>
        <div v-if="streaming" class="result-card__cursor">▌</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  content: { type: String, default: '' },
  streaming: { type: Boolean, default: false },
})

const CV_HEADER = '## CV adapté'
const LM_HEADER = '## Lettre de motivation adaptée'

const cvContent = computed(() => {
  const c = props.content
  const cvIdx = c.indexOf(CV_HEADER)
  if (cvIdx === -1) return c.trim()
  const start = c.indexOf('\n', cvIdx) + 1
  const lmIdx = c.indexOf(LM_HEADER)
  const end = lmIdx !== -1 ? lmIdx : c.length
  return c.slice(start, end).trim()
})

const lmContent = computed(() => {
  const c = props.content
  const lmIdx = c.indexOf(LM_HEADER)
  if (lmIdx === -1) return ''
  const start = c.indexOf('\n', lmIdx) + 1
  return c.slice(start).trim()
})

function renderMd(text) {
  return text ? marked.parse(text) : ''
}

const copiedKey = ref('')
function copy(text, key) {
  navigator.clipboard.writeText(text)
  copiedKey.value = key
  setTimeout(() => { copiedKey.value = '' }, 2000)
}

function download(markdownText, filename) {
  const html = marked.parse(markdownText)
  const doc = `<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40">
<head><meta charset="utf-8"><style>body{font-family:Arial,sans-serif;font-size:11pt;line-height:1.6;margin:2cm}h1,h2,h3{color:#1e293b}p{margin:0.5em 0}</style></head>
<body>${html}</body></html>`
  const blob = new Blob([doc], { type: 'application/msword' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${filename}.doc`
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.result-card {
  margin-top: 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}
.result-card__sections {
  display: grid;
  grid-template-columns: 1fr;
}
.result-card__sections--two-col {
  grid-template-columns: 1fr 1fr;
}
.result-card__section {
  border-right: 1px solid #e2e8f0;
}
.result-card__section:last-child { border-right: none; }

.result-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}
.result-card__label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
}
.result-card__actions {
  display: flex;
  gap: 0.4rem;
}
.result-card__copy,
.result-card__download {
  font-size: 0.8rem;
  padding: 0.25rem 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}
.result-card__copy:hover,
.result-card__download:hover { background: #f1f5f9; }
.result-card__download { border-color: #0ea5e9; color: #0369a1; }
.result-card__download:hover { background: #f0f9ff; }
.result-card__body {
  padding: 1rem;
  line-height: 1.7;
  font-size: 0.9rem;
}
.result-card__cursor {
  padding: 0 1rem 0.5rem;
  color: #0ea5e9;
  animation: blink 1s step-end infinite;
}
@keyframes blink { 50% { opacity: 0; } }

@media (max-width: 640px) {
  .result-card__sections--two-col {
    grid-template-columns: 1fr;
  }
  .result-card__section { border-right: none; border-bottom: 1px solid #e2e8f0; }
  .result-card__section:last-child { border-bottom: none; }
}
</style>
