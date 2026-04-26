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
      <div v-for="item in items" :key="item.id" class="item">
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
          </div>
        </div>
        <div class="item-right">
          <span class="item-badge">Généré</span>
          <button class="dl-btn" @click="download(item)">Télécharger</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { marked } from 'marked'
import { getHistory } from '../services/api'

const items = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    items.value = await getHistory()
  } finally {
    loading.value = false
  }
})

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

function download(item) {
  const html = marked.parse(item.output)
  const filename = item.agent === 'linkedin' ? 'post-linkedin' : 'cv-adapte'
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
  transition: border-color 0.2s, background 0.2s;
}
.item:hover { background: #1A2238; border-color: rgba(255,255,255,0.14); }

.item-left { display: flex; align-items: center; gap: 14px; min-width: 0; }

.item-ico {
  width: 38px; height: 38px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 17px;
  flex-shrink: 0;
}
.item-ico--li { background: rgba(0,229,255,0.1); }
.item-ico--cv { background: rgba(139,92,246,0.12); }

.item-meta { min-width: 0; }
.item-title {
  font-size: 13px;
  font-weight: 600;
  color: #D8E0F0;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.item-date { font-size: 11px; color: #6B7590; }

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

@media (max-width: 620px) {
  .container { padding: 36px 18px; }
  .item { flex-direction: column; align-items: flex-start; }
  .item-right { width: 100%; justify-content: flex-end; }
}
</style>
