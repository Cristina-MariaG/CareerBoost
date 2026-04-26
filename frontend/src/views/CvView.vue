<template>
  <div class="container">
    <div class="page-badge"><span class="badge-dot"></span> Agent IA — CV & Lettre</div>
    <h1>Adapte ton CV &<br><span>ta lettre</span></h1>
    <p class="subtitle">Colle l'offre d'emploi, dépose tes documents — <strong>ton agent IA fait le reste.</strong></p>

    <form @submit.prevent="submit">
      <div class="field">
        <label>Offre d'emploi</label>
        <textarea
          v-model="jobOffer"
          rows="6"
          placeholder="Colle ici le texte de l'offre d'emploi…"
          :disabled="streaming"
        />
      </div>

      <div class="drop-grid">
        <div>
          <label>CV <span class="tag-required">REQUIS</span></label>
          <FileUpload v-model="cvFile" label="Ton CV (PDF)" icon="📄" :disabled="streaming" />
        </div>
        <div>
          <label>Lettre <span class="tag-optional">OPTIONNEL</span></label>
          <FileUpload v-model="coverLetterFile" label="Ta lettre de motivation (PDF)" icon="✉️" :disabled="streaming" />
        </div>
      </div>

      <button class="cta-btn" type="submit" :disabled="streaming || !canSubmit">
        {{ streaming ? 'Adaptation en cours…' : 'Adapter mes documents →' }}
      </button>
    </form>

    <p v-if="error" class="error-msg">{{ error }}</p>

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
.container {
  max-width: 780px;
  margin: 0 auto;
  padding: 50px 40px;
}

.page-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(0,229,255,0.08);
  border: 1px solid rgba(0,229,255,0.2);
  border-radius: 100px;
  padding: 5px 13px;
  font-size: 11px;
  font-weight: 600;
  color: var(--cyan);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 20px;
}
.badge-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--cyan);
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
  background: linear-gradient(135deg, var(--cyan), var(--violet));
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
.subtitle strong { color: #C5CEDE; font-weight: 500; }

.field { margin-bottom: 24px; }

label {
  display: block;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #7B85A0;
  margin-bottom: 9px;
}
.tag-required { color: var(--pink); font-size: 10px; letter-spacing: 0.06em; font-weight: 700; margin-left: 4px; }
.tag-optional { color: #6B7590; font-size: 10px; letter-spacing: 0.06em; font-weight: 600; margin-left: 4px; }

textarea {
  width: 100%;
  background: var(--card);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 14px;
  color: #E8EEF8;
  font-family: var(--fb);
  font-size: 14px;
  font-weight: 300;
  line-height: 1.7;
  padding: 16px 18px;
  resize: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
textarea::placeholder { color: rgba(139,149,176,0.5); }
textarea:focus {
  outline: none;
  border-color: rgba(0,229,255,0.45);
  box-shadow: 0 0 0 3px rgba(0,229,255,0.07);
}

.drop-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 24px;
}

.cta-btn {
  width: 100%;
  background: linear-gradient(135deg, #00C8E0, #7C3AED);
  border: none;
  border-radius: 14px;
  color: #fff;
  font-family: var(--fh);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.03em;
  padding: 18px;
  cursor: pointer;
  transition: all 0.25s;
  box-shadow: 0 4px 24px rgba(0,200,224,0.18);
}
.cta-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 14px 40px rgba(0,200,224,0.35); filter: brightness(1.1); }
.cta-btn:active { transform: translateY(0); }
.cta-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.error-msg {
  margin-top: 1rem;
  color: #F87171;
  font-size: 0.9rem;
}

@media (max-width: 620px) {
  .container { padding: 36px 18px; }
  .drop-grid { grid-template-columns: 1fr; }
}
</style>
