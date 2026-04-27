<template>
  <div v-if="props.content || streaming" class="result-wrap">
    <div v-if="streaming && !props.content" class="spinner">
      <div class="spin"></div>
      <span>Ton agent IA analyse…</span>
    </div>

    <div v-else-if="props.content" class="result-grid" :class="{ 'result-grid--two': lmContent }">
      <div class="output-card">
        <div class="output-header">
          <span class="output-title">CV adapté</span>
          <div class="actions" v-if="cvContent">
            <button class="copy-btn" @click="copy(cvContent, 'cv')">{{ copiedKey === 'cv' ? 'Copié ✓' : 'Copier' }}</button>
            <button class="dl-btn" @click="download(cvContent, 'cv-adapte')">Télécharger</button>
          </div>
        </div>
        <div class="output-body" v-html="renderMd(cvContent)"></div>
        <div v-if="streaming && !lmContent" class="output-cursor">▌</div>
      </div>

      <div v-if="lmContent" class="output-card">
        <div class="output-header">
          <span class="output-title">Lettre de motivation</span>
          <div class="actions">
            <button class="copy-btn" @click="copy(lmContent, 'lm')">{{ copiedKey === 'lm' ? 'Copié ✓' : 'Copier' }}</button>
            <button class="dl-btn" @click="download(lmContent, 'lettre-motivation')">Télécharger</button>
          </div>
        </div>
        <div class="output-body" v-html="renderMd(lmContent)"></div>
        <div v-if="streaming" class="output-cursor">▌</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

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
  return c.slice(start, lmIdx !== -1 ? lmIdx : c.length).trim()
})

const lmContent = computed(() => {
  const c = props.content
  const lmIdx = c.indexOf(LM_HEADER)
  if (lmIdx === -1) return ''
  return c.slice(c.indexOf('\n', lmIdx) + 1).trim()
})

function renderMd(text) {
  return text ? DOMPurify.sanitize(marked.parse(text)) : ''
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
.result-wrap { margin-top: 28px; animation: fadeIn 0.4s ease; }
@keyframes fadeIn { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }

.spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 28px;
  color: var(--text-muted);
  font-size: 14px;
  background: var(--card);
  border: 1px solid rgba(0,229,255,0.22);
  border-radius: 18px;
}
.spin {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(0,229,255,0.15);
  border-top-color: var(--cyan);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.result-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
}
.result-grid--two { grid-template-columns: 1fr 1fr; }

.output-card {
  background: var(--card);
  border: 1px solid rgba(0,229,255,0.22);
  border-radius: 18px;
  overflow: hidden;
}

.output-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  background: rgba(0,229,255,0.06);
  border-bottom: 1px solid rgba(255,255,255,0.07);
}
.output-title {
  font-family: var(--fh);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--cyan);
}
.actions { display: flex; gap: 6px; }

.copy-btn {
  background: rgba(255,255,255,0.09);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 8px;
  color: #fff;
  font-family: var(--fb);
  font-size: 12px;
  font-weight: 600;
  padding: 5px 13px;
  cursor: pointer;
  transition: all 0.2s;
}
.copy-btn:hover { background: rgba(0,229,255,0.18); color: var(--cyan); border-color: rgba(0,229,255,0.4); }

.dl-btn {
  background: rgba(0,229,255,0.08);
  border: 1px solid rgba(0,229,255,0.3);
  border-radius: 8px;
  color: var(--cyan);
  font-family: var(--fb);
  font-size: 12px;
  font-weight: 600;
  padding: 5px 13px;
  cursor: pointer;
  transition: all 0.2s;
}
.dl-btn:hover { background: rgba(0,229,255,0.18); }

.output-body {
  padding: 22px;
  font-size: 14px;
  line-height: 1.85;
  color: var(--text-body);
}
.output-body :deep(p) { margin-bottom: 0.75rem; }
.output-body :deep(strong) { color: var(--text); }
.output-body :deep(h1), .output-body :deep(h2), .output-body :deep(h3) {
  font-family: var(--fh);
  color: var(--text);
  margin: 1rem 0 0.5rem;
}

.output-cursor {
  padding: 0 22px 12px;
  color: var(--cyan);
  animation: blink 1s step-end infinite;
}
@keyframes blink { 50% { opacity: 0; } }

@media (max-width: 620px) {
  .result-grid--two { grid-template-columns: 1fr; }
}
</style>
