<template>
  <div
    class="file-upload"
    :class="{ 'file-upload--dragover': dragover, 'file-upload--has-file': modelValue, 'file-upload--error': errorMsg }"
    @dragover.prevent="dragover = true"
    @dragleave="dragover = false"
    @drop.prevent="onDrop"
    @click="$refs.input.click()"
  >
    <input ref="input" type="file" accept=".pdf" hidden @change="onChange" />

    <div v-if="modelValue" class="file-upload__file">
      <span class="file-upload__filename">{{ modelValue.name }}</span>
      <button class="file-upload__remove" type="button" @click.stop="clear">×</button>
    </div>
    <div v-else class="file-upload__placeholder">
      <span class="file-upload__label">{{ label }}</span>
      <span class="file-upload__hint">Glisse un PDF ici ou clique pour choisir</span>
    </div>

    <p v-if="errorMsg" class="file-upload__error">{{ errorMsg }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: { type: File, default: null },
  label: { type: String, default: 'Fichier PDF' },
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
.file-upload {
  border: 2px dashed #cbd5e1;
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
  min-height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.file-upload:hover { border-color: #94a3b8; background: #f8fafc; }
.file-upload--dragover { border-color: #0ea5e9; background: #f0f9ff; }
.file-upload--has-file { border-style: solid; border-color: #0ea5e9; background: #f0f9ff; }
.file-upload--error { border-color: #ef4444; }

.file-upload__placeholder {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.file-upload__label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
}
.file-upload__hint {
  font-size: 0.8rem;
  color: #94a3b8;
}
.file-upload__file {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.file-upload__filename {
  font-size: 0.9rem;
  font-weight: 500;
  color: #0369a1;
  word-break: break-all;
}
.file-upload__remove {
  background: none;
  border: none;
  color: #64748b;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0 0.25rem;
  line-height: 1;
}
.file-upload__remove:hover { color: #ef4444; }
.file-upload__error {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #ef4444;
}
</style>
