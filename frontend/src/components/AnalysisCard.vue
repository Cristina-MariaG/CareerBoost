<template>
  <div class="analysis-card">
    <div v-if="streaming" class="streaming-indicator">
      <span class="dot" /><span class="dot" /><span class="dot" />
    </div>
    <div class="analysis-content" v-html="renderedContent" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const props = defineProps({
  content: { type: String, default: '' },
  streaming: { type: Boolean, default: false },
})

const renderedContent = computed(() => DOMPurify.sanitize(marked.parse(props.content + (props.streaming ? '▍' : ''))))
</script>

<style scoped>
.analysis-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 2rem;
  margin-top: 2rem;
}

.streaming-indicator {
  display: flex;
  gap: 6px;
  margin-bottom: 1rem;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--cyan);
  animation: pulse 1.2s ease-in-out infinite;
}
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes pulse {
  0%, 100% { opacity: 0.3; transform: scale(0.8); }
  50% { opacity: 1; transform: scale(1); }
}

.analysis-content :deep(h2) {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--cyan);
  margin: 1.5rem 0 0.75rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--border);
}
.analysis-content :deep(h2:first-child) { margin-top: 0; }

.analysis-content :deep(ul) {
  list-style: none;
  padding: 0;
  margin: 0 0 0.5rem;
}

.analysis-content :deep(ul li) {
  padding: 0.35rem 0 0.35rem 1.4rem;
  position: relative;
  color: var(--text-muted);
  font-size: 0.95rem;
  line-height: 1.5;
}

.analysis-content :deep(ul li::before) {
  content: '→';
  position: absolute;
  left: 0;
  color: var(--violet);
}

.analysis-content :deep(p) {
  color: var(--text-muted);
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0.5rem 0;
}

.analysis-content :deep(strong) {
  color: var(--text);
}
</style>
