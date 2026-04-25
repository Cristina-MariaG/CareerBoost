<template>
  <div class="linkedin-view">
    <h1 class="linkedin-view__title">Générateur de post LinkedIn</h1>

    <form class="linkedin-view__form" @submit.prevent="submit">
      <label class="linkedin-view__label">Description</label>
      <textarea
        v-model="description"
        class="linkedin-view__textarea"
        placeholder="Décris ce que tu veux partager : projet, apprentissage, expérience..."
        rows="6"
        :disabled="streaming"
      />

      <label class="linkedin-view__label">Ton</label>
      <div class="linkedin-view__tones">
        <button
          v-for="t in tones"
          :key="t.value"
          type="button"
          class="linkedin-view__tone"
          :class="{ 'linkedin-view__tone--active': tone === t.value }"
          :disabled="streaming"
          @click="tone = t.value"
        >
          {{ t.label }}
        </button>
      </div>

      <button class="linkedin-view__submit" type="submit" :disabled="streaming || !description.trim()">
        {{ streaming ? 'Génération en cours...' : 'Générer le post' }}
      </button>
    </form>

    <p v-if="error" class="linkedin-view__error">{{ error }}</p>

    <PostResult :content="result" :streaming="streaming" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { streamLinkedIn } from '../services/api'
import PostResult from '../components/PostResult.vue'

const tones = [
  { value: 'professionnel', label: 'Professionnel' },
  { value: 'storytelling', label: 'Storytelling' },
  { value: 'technique', label: 'Technique' },
]

const description = ref('')
const tone = ref('professionnel')
const result = ref('')
const streaming = ref(false)
const error = ref('')

async function submit() {
  if (!description.value.trim()) return
  error.value = ''
  result.value = ''
  streaming.value = true

  await streamLinkedIn({
    description: description.value,
    tone: tone.value,
    onChunk: (text) => { result.value += text },
    onDone: () => { streaming.value = false },
    onError: (err) => { error.value = typeof err === 'string' ? err : 'Une erreur est survenue.'; streaming.value = false },
  })
}
</script>

<style scoped>
.linkedin-view {
  max-width: 680px;
  margin: 2rem auto;
  padding: 0 1rem;
}
.linkedin-view__title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #1e293b;
}
.linkedin-view__form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.linkedin-view__label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
}
.linkedin-view__textarea {
  padding: 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.95rem;
  resize: vertical;
  font-family: inherit;
}
.linkedin-view__textarea:focus {
  outline: none;
  border-color: #0ea5e9;
}
.linkedin-view__tones {
  display: flex;
  gap: 0.5rem;
}
.linkedin-view__tone {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.15s;
}
.linkedin-view__tone--active {
  background: #0ea5e9;
  color: white;
  border-color: #0ea5e9;
}
.linkedin-view__tone:hover:not(.linkedin-view__tone--active):not(:disabled) {
  background: #f1f5f9;
}
.linkedin-view__submit {
  padding: 0.75rem;
  background: #0ea5e9;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}
.linkedin-view__submit:hover:not(:disabled) { background: #0284c7; }
.linkedin-view__submit:disabled { opacity: 0.6; cursor: not-allowed; }
.linkedin-view__error {
  margin-top: 1rem;
  color: #ef4444;
  font-size: 0.9rem;
}
</style>
