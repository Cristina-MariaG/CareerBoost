<template>
  <div class="container">
    <div class="page-badge"><span class="badge-dot"></span> Agent IA — LinkedIn</div>
    <h1>Génère ton post<br><span>LinkedIn parfait</span></h1>
    <p class="subtitle">Décris ton idée, choisis le ton — <strong>ton agent IA fait le reste.</strong></p>

    <form @submit.prevent="submit">
      <div class="field">
        <label>Ton idée</label>
        <textarea
          v-model="description"
          rows="6"
          placeholder="Ex : J'ai lancé un side project en 3 semaines, voici ce que j'ai appris…"
          :disabled="streaming"
        />
      </div>

      <div class="field">
        <label>Ton</label>
        <div class="tone-grid">
          <button
            v-for="t in tones"
            :key="t.value"
            type="button"
            class="tone-btn"
            :class="{ 'tone-btn--active': tone === t.value }"
            :disabled="streaming"
            @click="tone = t.value"
          >
            <span class="tone-icon">{{ t.icon }}</span>{{ t.label }}
          </button>
        </div>
      </div>

      <button class="cta-btn" type="submit" :disabled="streaming || description.trim().length < 10">
        {{ streaming ? 'Génération en cours…' : 'Générer le post →' }}
      </button>
    </form>

    <p v-if="error" class="error-msg">{{ error }}</p>

    <PostResult :content="result" :streaming="streaming" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { streamLinkedIn } from '../services/api'
import PostResult from '../components/PostResult.vue'

const tones = [
  { value: 'professionnel', label: 'Professionnel', icon: '🎯' },
  { value: 'storytelling', label: 'Storytelling', icon: '✨' },
  { value: 'technique', label: 'Technique', icon: '⚙️' },
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
    onError: (err) => {
      if (typeof err === 'string') error.value = err
      else if (err?.description?.[0]) error.value = err.description[0]
      else if (err?.tone?.[0]) error.value = err.tone[0]
      else error.value = 'Une erreur est survenue.'
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

.tone-grid { display: flex; gap: 10px; }
.tone-btn {
  flex: 1;
  background: var(--card2);
  border: 2px solid rgba(255,255,255,0.22);
  border-radius: 14px;
  color: #fff;
  font-family: var(--fb);
  font-size: 14px;
  font-weight: 700;
  padding: 18px 10px;
  cursor: pointer;
  transition: all 0.22s;
}
.tone-btn:hover:not(:disabled) {
  background: #fff;
  border-color: #fff;
  color: var(--bg);
}
.tone-btn--active {
  background: rgba(0,229,255,0.15);
  border-color: var(--cyan);
  color: var(--cyan);
  box-shadow: 0 0 22px rgba(0,229,255,0.12);
}
.tone-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.tone-icon { display: block; font-size: 22px; margin-bottom: 8px; }

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
  .tone-grid { flex-direction: column; }
}
</style>
