<template>
  <div class="cv-view">
    <h1 class="cv-view__title">Adaptateur CV & Lettre de motivation</h1>

    <form class="cv-view__form" @submit.prevent="submit">
      <label class="cv-view__label">Offre d'emploi</label>
      <textarea
        v-model="jobOffer"
        class="cv-view__textarea"
        placeholder="Colle ici le texte de l'offre d'emploi..."
        rows="6"
        :disabled="streaming"
      />

      <div class="cv-view__uploads">
        <div class="cv-view__upload-group">
          <label class="cv-view__label">CV <span class="cv-view__required">*</span></label>
          <FileUpload v-model="cvFile" label="Ton CV (PDF)" :disabled="streaming" />
        </div>

        <div class="cv-view__upload-group">
          <label class="cv-view__label">Lettre de motivation <span class="cv-view__optional">optionnel</span></label>
          <FileUpload v-model="coverLetterFile" label="Ta lettre de motivation (PDF)" :disabled="streaming" />
        </div>
      </div>

      <button
        class="cv-view__submit"
        type="submit"
        :disabled="streaming || !canSubmit"
      >
        {{ streaming ? 'Génération en cours...' : 'Adapter mes documents' }}
      </button>
    </form>

    <p v-if="error" class="cv-view__error">{{ error }}</p>

    <ResultCard :content="result" :streaming="streaming" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { streamCv } from '../services/api'
import FileUpload from '../components/FileUpload.vue'
import ResultCard from '../components/ResultCard.vue'

const jobOffer = ref('')
const cvFile = ref(null)
const coverLetterFile = ref(null)
const result = ref('')
const streaming = ref(false)
const error = ref('')

const canSubmit = computed(() => jobOffer.value.trim().length >= 20 && cvFile.value !== null)

async function submit() {
  if (!canSubmit.value) return
  error.value = ''
  result.value = ''
  streaming.value = true

  await streamCv({
    job_offer: jobOffer.value,
    cv: cvFile.value,
    cover_letter: coverLetterFile.value,
    onChunk: (text) => { result.value += text },
    onDone: () => { streaming.value = false },
    onError: (err) => {
      error.value = typeof err === 'string' ? err : (err?.job_offer?.[0] || err?.cv?.[0] || 'Une erreur est survenue.')
      streaming.value = false
    },
  })
}
</script>

<style scoped>
.cv-view {
  max-width: 860px;
  margin: 2rem auto;
  padding: 0 1rem;
}
.cv-view__title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #1e293b;
}
.cv-view__form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.cv-view__label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
}
.cv-view__required { color: #ef4444; }
.cv-view__optional {
  font-weight: 400;
  font-size: 0.8rem;
  color: #94a3b8;
}
.cv-view__textarea {
  padding: 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.95rem;
  resize: vertical;
  font-family: inherit;
}
.cv-view__textarea:focus {
  outline: none;
  border-color: #0ea5e9;
}
.cv-view__uploads {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
.cv-view__upload-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.cv-view__submit {
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
.cv-view__submit:hover:not(:disabled) { background: #0284c7; }
.cv-view__submit:disabled { opacity: 0.6; cursor: not-allowed; }
.cv-view__error {
  margin-top: 1rem;
  color: #ef4444;
  font-size: 0.9rem;
}

@media (max-width: 640px) {
  .cv-view__uploads { grid-template-columns: 1fr; }
}
</style>
