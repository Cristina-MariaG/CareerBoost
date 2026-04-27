<template>
  <div
    class="drop-zone"
    :class="{ 'drop-zone--dragover': dragover, 'drop-zone--has-file': modelValue, 'drop-zone--error': errorMsg, 'drop-zone--disabled': disabled }"
    @dragover.prevent="!disabled && (dragover = true)"
    @dragleave="dragover = false"
    @drop.prevent="!disabled && onDrop($event)"
    @click="!disabled && $refs.input.click()"
  >
    <input ref="input" type="file" accept=".pdf" hidden @change="onChange" />

    <template v-if="modelValue">
      <span class="drop-icon">✓</span>
      <div class="drop-label" style="color: var(--cyan)">{{ modelValue.name }}</div>
      <button class="drop-remove" type="button" @click.stop="clear">Supprimer</button>
    </template>
    <template v-else>
      <span class="drop-icon">{{ icon }}</span>
      <div class="drop-label">{{ label }}</div>
      <div class="drop-hint">Glisse ou clique pour choisir</div>
    </template>

    <p v-if="errorMsg" class="drop-error">{{ errorMsg }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  modelValue: { type: File, default: null },
  label: { type: String, default: 'Fichier PDF' },
  icon: { type: String, default: '📄' },
  disabled: { type: Boolean, default: false },
})
const emit = defineEmits(['update:modelValue'])

const dragover = ref(false)
const errorMsg = ref('')

function validate(file) {
  if (!file.name.toLowerCase().endsWith('.pdf')) {
    errorMsg.value = 'Le fichier doit être un PDF.'
    return false
  }
  if (file.size > 5 * 1024 * 1024) {
    errorMsg.value = 'Le fichier ne doit pas dépasser 5 Mo.'
    return false
  }
  errorMsg.value = ''
  return true
}

function onChange(e) {
  const file = e.target.files[0]
  if (file && validate(file)) emit('update:modelValue', file)
  e.target.value = ''
}

function onDrop(e) {
  dragover.value = false
  const file = e.dataTransfer.files[0]
  if (file && validate(file)) emit('update:modelValue', file)
}

function clear() {
  errorMsg.value = ''
  emit('update:modelValue', null)
}
</script>

<style scoped>
.drop-zone {
  background: var(--card2);
  border: 2px dashed rgba(255,255,255,0.18);
  border-radius: 14px;
  padding: 28px 16px;
  text-align: center;
  cursor: pointer;
  transition: all 0.22s;
  min-height: 110px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
}
.drop-zone:hover { border-color: rgba(0,229,255,0.5); background: #1A2D50; }
.drop-zone--dragover { border-color: var(--cyan); background: rgba(0,229,255,0.05); }
.drop-zone--has-file { border-style: solid; border-color: var(--cyan); background: rgba(0,229,255,0.05); }
.drop-zone--error { border-color: #F87171; }
.drop-zone--disabled { opacity: 0.5; cursor: not-allowed; }

.drop-icon { font-size: 26px; display: block; }
.drop-label {
  font-family: var(--fh);
  font-size: 13px;
  font-weight: 700;
  color: #D8E0F0;
  word-break: break-all;
}
.drop-hint { font-size: 11px; color: var(--text-muted); }

.drop-remove {
  background: rgba(248,113,113,0.1);
  border: 1px solid rgba(248,113,113,0.3);
  border-radius: 6px;
  color: #F87171;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  cursor: pointer;
  margin-top: 4px;
  transition: all 0.2s;
}
.drop-remove:hover { background: rgba(248,113,113,0.2); }

.drop-error {
  font-size: 11px;
  color: #F87171;
  margin-top: 6px;
}
</style>
