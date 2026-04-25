<template>
  <div v-if="content" class="post-result">
    <div class="post-result__header">
      <span class="post-result__label">Post généré</span>
      <button class="post-result__copy" @click="copy">{{ copied ? 'Copié !' : 'Copier' }}</button>
    </div>
    <div class="post-result__body" v-html="renderedMarkdown"></div>
    <div v-if="streaming" class="post-result__cursor">▌</div>
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
.post-result {
  margin-top: 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}
.post-result__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}
.post-result__label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
}
.post-result__copy {
  font-size: 0.8rem;
  padding: 0.25rem 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}
.post-result__copy:hover { background: #f1f5f9; }
.post-result__body {
  padding: 1rem;
  line-height: 1.7;
  white-space: pre-wrap;
}
.post-result__cursor {
  padding: 0 1rem 0.5rem;
  color: #0ea5e9;
  animation: blink 1s step-end infinite;
}
@keyframes blink { 50% { opacity: 0; } }
</style>
