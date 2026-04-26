<template>
  <div v-if="content || streaming" class="output-card">
    <div v-if="streaming && !content" class="spinner">
      <div class="spin"></div>
      <span>Ton agent IA rédige…</span>
    </div>
    <template v-else-if="content">
      <div class="output-header">
        <span class="output-title">Post LinkedIn</span>
        <button class="copy-btn" @click="copy">{{ copied ? 'Copié ✓' : 'Copier' }}</button>
      </div>
      <div class="output-body" v-html="renderedMarkdown"></div>
      <div v-if="streaming" class="output-cursor">▌</div>
    </template>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  content: { type: String, default: '' },
  streaming: { type: Boolean, default: false },
})

const renderedMarkdown = computed(() => marked.parse(props.content))

const copied = ref(false)
function copy() {
  navigator.clipboard.writeText(props.content)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}
</script>

<style scoped>
.output-card {
  margin-top: 28px;
  background: var(--card);
  border: 1px solid rgba(0,229,255,0.22);
  border-radius: 18px;
  overflow: hidden;
  animation: fadeIn 0.4s ease;
}
@keyframes fadeIn { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }

.spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 28px;
  color: var(--text-muted);
  font-size: 14px;
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
.copy-btn:hover {
  background: rgba(0,229,255,0.18);
  color: var(--cyan);
  border-color: rgba(0,229,255,0.4);
}

.output-body {
  padding: 22px;
  font-size: 14px;
  line-height: 1.85;
  color: var(--text-body);
}
.output-body :deep(p) { margin-bottom: 0.75rem; }
.output-body :deep(strong) { color: var(--text); }

.output-cursor {
  padding: 0 22px 12px;
  color: var(--cyan);
  animation: blink 1s step-end infinite;
}
@keyframes blink { 50% { opacity: 0; } }
</style>
