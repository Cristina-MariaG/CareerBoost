<template>
  <div class="container">
    <div class="page-badge"><span class="badge-dot"></span> Historique</div>
    <h1>Tes <span>générations</span></h1>
    <p class="subtitle">Retrouve tes posts et documents générés lors de cette session.</p>

    <div v-if="loading" class="spinner">
      <div class="spin"></div>
      <span>Chargement…</span>
    </div>

    <div v-else-if="items.length === 0" class="empty">
      <span class="empty-icon">📭</span>
      <p>Aucune génération pour cette session.</p>
    </div>

    <div v-else class="list">
      <div v-for="item in items" :key="item.id" class="item" @click="open(item)">
        <div class="item-left">
          <div class="item-ico" :class="item.agent === 'linkedin' ? 'item-ico--li' : 'item-ico--cv'">
            {{ item.agent === 'linkedin' ? '💼' : '📄' }}
          </div>
          <div class="item-meta">
            <div class="item-title">
              {{ item.agent === 'linkedin'
                ? `Post LinkedIn — ton ${item.input_data.tone}`
                : `CV adapté — ${item.input_data.job_offer?.slice(0, 50)}…` }}
            </div>
            <div class="item-date">{{ formatDate(item.created_at) }}</div>
            <div class="item-preview">{{ item.preview }}</div>
          </div>
        </div>
        <div class="item-right">
          <span class="item-badge">Généré</span>
          <template v-if="item.agent === 'cv'">
            <button class="dl-btn" @click.stop="downloadPart(cvContent(item.output), 'cv-adapte')">CV</button>
            <button v-if="lmContent(item.output)" class="dl-btn" @click.stop="downloadPart(lmContent(item.output), 'lettre-motivation')">LM</button>
          </template>
          <button v-else class="dl-btn" @click.stop="downloadPart(item.output, 'post-linkedin')">Télécharger</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal -->
  <Teleport to="body">
    <div v-if="selected" class="modal-backdrop" @click.self="close">
      <div class="modal">
        <div class="modal-header">
          <div class="modal-title-wrap">
            <span class="modal-ico" :class="selected.agent === 'linkedin' ? 'modal-ico--li' : 'modal-ico--cv'">
              {{ selected.agent === 'linkedin' ? '💼' : '📄' }}
            </span>
            <span class="modal-title">
              {{ selected.agent === 'linkedin'
                ? `Post LinkedIn — ton ${selected.input_data.tone}`
                : 'CV adapté' }}
            </span>
          </div>
          <div class="modal-actions">
            <button class="copy-btn" @click="copy(selected.output)">{{ copied ? 'Copié ✓' : 'Copier' }}</button>
            <template v-if="selected.agent === 'cv'">
              <button class="dl-btn" @click="downloadPart(cvContent(selected.output), 'cv-adapte')">CV</button>
              <button v-if="lmContent(selected.output)" class="dl-btn" @click="downloadPart(lmContent(selected.output), 'lettre-motivation')">LM</button>
            </template>
            <button v-else class="dl-btn" @click="downloadPart(selected.output, 'post-linkedin')">Télécharger</button>
            <button class="close-btn" @click="close">✕</button>
          </div>
        </div>
        <div class="modal-body">
          <div v-if="selected.input_data?.job_offer" class="modal-offer">
            <div class="modal-offer-label">Offre d'emploi</div>
            <div class="modal-offer-text">{{ selected.input_data.job_offer }}</div>
          </div>
          <div v-html="renderMd(selected.output)"></div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { marked } from 'marked'
import { getHistory } from '../services/api'

const items = ref([])
const loading = ref(true)
const selected = ref(null)
const copied = ref(false)

onMounted(async () => {
  try {
    items.value = await getHistory()
    console.log('[history]', JSON.stringify(items.value.map(i => ({ agent: i.agent, input_data: i.input_data }))))
  } finally {
    loading.value = false
  }
  window.addEventListener('keydown', onKey)
})
onUnmounted(() => window.removeEventListener('keydown', onKey))

function onKey(e) {
  if (e.key === 'Escape') close()
}

function open(item) { selected.value = item }
function close() { selected.value = null; copied.value = false }

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

const CV_HEADER = '## CV adapté'
const LM_HEADER = '## Lettre de motivation adaptée'

function cvContent(output) {
  const cvIdx = output.indexOf(CV_HEADER)
  if (cvIdx === -1) return output.trim()
  const start = output.indexOf('\n', cvIdx) + 1
  const lmIdx = output.indexOf(LM_HEADER)
  return output.slice(start, lmIdx !== -1 ? lmIdx : output.length).trim()
}

function lmContent(output) {
  const lmIdx = output.indexOf(LM_HEADER)
  if (lmIdx === -1) return ''
  return output.slice(output.indexOf('\n', lmIdx) + 1).trim()
}

function renderMd(text) {
  return text ? marked.parse(text) : ''
}

function copy(text) {
  navigator.clipboard.writeText(text)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}

function downloadPart(text, filename) {
  const html = marked.parse(text)
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
.container {
  max-width: 780px;
  margin: 0 auto;
  padding: 50px 40px;
}

.page-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(139,92,246,0.08);
  border: 1px solid rgba(139,92,246,0.2);
  border-radius: 100px;
  padding: 5px 13px;
  font-size: 11px;
  font-weight: 600;
  color: var(--violet);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 20px;
}
.badge-dot {
  width: 5px; height: 5px;
  border-radius: 50%;
  background: var(--violet);
  animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

h1 {
  font-family: var(--fh);
  font-size: clamp(28px, 4vw, 44px);
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -0.5px;
  margin-bottom: 10px;
  color: #fff;
}
h1 span {
  background: linear-gradient(135deg, var(--violet), var(--pink));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: var(--text-muted);
  font-size: 15px;
  font-weight: 300;
  line-height: 1.6;
  margin-bottom: 40px;
}

.spinner {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-muted);
  font-size: 14px;
  padding: 40px 0;
}
.spin {
  width: 18px; height: 18px;
  border: 2px solid rgba(139,92,246,0.15);
  border-top-color: var(--violet);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 60px 0;
  color: var(--text-muted);
  font-size: 15px;
}
.empty-icon { font-size: 40px; }

.list { display: flex; flex-direction: column; gap: 10px; }

.item {
  background: var(--card);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 14px;
  padding: 16px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}
.item:hover { background: #1A2238; border-color: rgba(139,92,246,0.3); }

.item-left { display: flex; align-items: flex-start; gap: 14px; min-width: 0; flex: 1; }

.item-ico {
  width: 38px; height: 38px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 17px;
  flex-shrink: 0;
}
.item-ico--li { background: rgba(0,229,255,0.1); }
.item-ico--cv { background: rgba(139,92,246,0.12); }

.item-meta { min-width: 0; flex: 1; }
.item-title {
  font-size: 13px;
  font-weight: 600;
  color: #D8E0F0;
  margin-bottom: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.item-date { font-size: 11px; color: #6B7590; margin-bottom: 6px; }
.item-preview {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-right { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }

.item-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 20px;
  background: rgba(74,222,128,0.1);
  color: #4ADE80;
  border: 1px solid rgba(74,222,128,0.2);
  white-space: nowrap;
}

.dl-btn {
  background: rgba(139,92,246,0.1);
  border: 1px solid rgba(139,92,246,0.3);
  border-radius: 8px;
  color: var(--violet);
  font-family: var(--fb);
  font-size: 12px;
  font-weight: 600;
  padding: 5px 13px;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}
.dl-btn:hover { background: rgba(139,92,246,0.2); }

/* Modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 100;
  background: rgba(4,6,12,0.85);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  animation: fadeIn 0.2s ease;
}
@keyframes fadeIn { from{opacity:0} to{opacity:1} }

.modal {
  background: var(--card);
  border: 1px solid rgba(139,92,246,0.25);
  border-radius: 20px;
  width: 100%;
  max-width: 740px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  animation: slideUp 0.25s ease;
}
@keyframes slideUp { from{transform:translateY(20px);opacity:0} to{transform:translateY(0);opacity:1} }

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.07);
  background: rgba(139,92,246,0.06);
  border-radius: 20px 20px 0 0;
  gap: 12px;
}
.modal-title-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}
.modal-ico {
  width: 32px; height: 32px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 15px;
  flex-shrink: 0;
}
.modal-ico--li { background: rgba(0,229,255,0.1); }
.modal-ico--cv { background: rgba(139,92,246,0.12); }

.modal-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.modal-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

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

.close-btn {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 8px;
  color: var(--text-muted);
  font-size: 14px;
  padding: 5px 10px;
  cursor: pointer;
  transition: all 0.2s;
  line-height: 1;
}
.close-btn:hover { background: rgba(248,113,113,0.15); color: #F87171; border-color: rgba(248,113,113,0.3); }

.modal-body {
  padding: 24px;
  overflow-y: auto;
  font-size: 14px;
  line-height: 1.85;
  color: var(--text-body);
}
.modal-body :deep(p) { margin-bottom: 0.75rem; }
.modal-body :deep(strong) { color: var(--text); }
.modal-body :deep(h1), .modal-body :deep(h2), .modal-body :deep(h3) {
  font-family: var(--fh);
  color: var(--text);
  margin: 1.2rem 0 0.5rem;
}
.modal-offer {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  padding: 14px 16px;
  margin-bottom: 24px;
}
.modal-offer-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #6B7590;
  margin-bottom: 8px;
}
.modal-offer-text {
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.6;
  white-space: pre-wrap;
  max-height: 160px;
  overflow-y: auto;
}

.modal-body :deep(ul), .modal-body :deep(ol) {
  padding-left: 1.5rem;
  margin-bottom: 0.75rem;
}

@media (max-width: 620px) {
  .container { padding: 36px 18px; }
  .item { flex-direction: column; align-items: flex-start; }
  .item-right { width: 100%; justify-content: flex-end; }
  .modal { max-height: 90vh; }
  .modal-header { flex-direction: column; align-items: flex-start; }
  .modal-actions { width: 100%; justify-content: flex-end; }
}
</style>
