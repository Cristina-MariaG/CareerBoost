# ROADMAP

## Ordre des branches

```
chore/project-init          ✅ terminé
feat/claude-client          ✅ terminé
feat/linkedin-agent-api     ✅ terminé
feat/linkedin-agent-ui      ✅ terminé
feat/pdf-handling           ✅ terminé
feat/cv-agent-api           ✅ terminé
feat/cv-agent-ui            ✅ terminé
chore/docker-prod
feat/frontend-design
feat/dashboard
feat/cv-analysis
```

---

## Milestone 1 — Foundation
> Done quand : `docker compose up` démarre backend + frontend, les deux services communiquent.

| # | Tâche | Branche |
|---|-------|---------|
| 1 | Init Django 5 + DRF + structure `config/`, `agents/` | `chore/project-init` |
| 2 | Init Vue.js 3 + Vite + Vue Router + Axios | `chore/project-init` |
| 3 | `docker-compose.yml` — backend + frontend + PostgreSQL + volume media | `chore/project-init` |
| 4 | Stratégie `.env` — toutes les variables (API key, DB, CORS, BACKEND_URL) | `chore/project-init` |
| 5 | CORS config Django (whitelist `http://localhost:5173`) | `chore/project-init` |

---

## Milestone 2 — Claude Integration Core
> Done quand : appel Claude réussi depuis un test, streaming SSE fonctionnel, prompt caching actif.

| # | Tâche | Branche |
|---|-------|---------|
| 6 | `claude_client.py` — wrapper SDK (`claude-sonnet-4-6`, streaming SSE, prompt caching) | `feat/claude-client` |
| 7 | Gestion d'erreurs : rate limit, timeout, clé invalide, réponse vide | `feat/claude-client` |
| 8 | Test de connectivité + validation caching | `feat/claude-client` |

---

## Milestone 3 — Agent LinkedIn (end-to-end)
> Done quand : depuis l'UI, soumettre une description → recevoir un post LinkedIn streamé en Markdown.

| # | Tâche | Branche |
|---|-------|---------|
| 9 | Modèle `Session` (UUID anonyme) + `GenerationHistory` | `feat/linkedin-agent-api` |
| 10 | `linkedin_agent.py` — prompt engineering, 3 tons | `feat/linkedin-agent-api` |
| 11 | Endpoint `POST /api/agents/linkedin/` + serializer + SSE | `feat/linkedin-agent-api` |
| 12 | Tests unitaires LinkedIn agent | `feat/linkedin-agent-api` |
| 13 | `LinkedinView.vue` — formulaire + sélecteur de ton | `feat/linkedin-agent-ui` |
| 14 | `PostResult.vue` — rendu Markdown streamé | `feat/linkedin-agent-ui` |
| 15 | `api.js` — gestion SSE, états loading / error / success | `feat/linkedin-agent-ui` |

---

## Milestone 4 — PDF Handling (isolé)
> Done quand : upload PDF → texte extrait proprement → fichier supprimé.

| # | Tâche | Branche |
|---|-------|---------|
| 16 | Upload Django multipart (FileField, `MEDIA_ROOT`, volume Docker) | `feat/pdf-handling` |
| 17 | Extraction texte PDF (`pdfplumber`) | `feat/pdf-handling` |
| 18 | Validation : taille max, type MIME, suppression post-traitement | `feat/pdf-handling` |

---

## Milestone 5 — Agent CV & LM (end-to-end)
> Done quand : upload offre + PDF → CV + LM adaptés streamés en Markdown.

| # | Tâche | Branche |
|---|-------|---------|
| 19 | `cv_agent.py` — prompt engineering (offre + contenu PDF) | `feat/cv-agent-api` |
| 20 | Endpoint `POST /api/agents/cv/` + serializer + SSE | `feat/cv-agent-api` |
| 21 | Historique session pour agent CV | `feat/cv-agent-api` |
| 22 | Tests unitaires CV agent | `feat/cv-agent-api` |
| 23 | `CvView.vue` — champ offre d'emploi + zone upload | `feat/cv-agent-ui` |
| 24 | `FileUpload.vue` — drag & drop, feedback erreur | `feat/cv-agent-ui` |
| 25 | `ResultCard.vue` — affichage CV + LM côte à côte, Markdown streamé | `feat/cv-agent-ui` |
| 26 | `api.js` — appel CV avec FormData + SSE | `feat/cv-agent-ui` |

---

## Milestone 6 — Production Ready
> Done quand : `docker compose up` en prod, les deux agents fonctionnent.

| # | Tâche | Branche |
|---|-------|---------|
| 27 | Docker prod config (gunicorn, nginx, env secrets) | `chore/docker-prod` |
| 28 | PostgreSQL prod + migrations | `chore/docker-prod` |
| 29 | README — instructions lancement dev + prod | `chore/docker-prod` |

---

---

## Milestone 7 — Dashboard & Historique
> Done quand : l'utilisateur peut consulter ses générations passées et re-télécharger les outputs.

| # | Tâche | Branche |
|---|-------|---------|
| 43 | Backend : endpoint `GET /api/history/` — historique de session paginé | `feat/dashboard` |
| 44 | Backend : `GenerationHistorySerializer` | `feat/dashboard` |
| 45 | Frontend : `HistoryView.vue` — liste des générations (date, type, aperçu) | `feat/dashboard` |
| 46 | Frontend : bouton re-télécharger output depuis l'historique (DOCX) | `feat/dashboard` |
| 47 | Frontend : lien "Historique" dans la navigation | `feat/dashboard` |
| 48 | Router : ajout route `/history` | `feat/dashboard` |

---

---

## Milestone 8 — Analyse & Recommandations CV
> Done quand : toggle Adapter/Analyser sur la page CV — mode analyse retourne points forts + recommandations concrètes.

| # | Tâche | Branche |
|---|-------|---------|
| 49 | Backend : champ `mode` (`adapt`\|`analyze`) dans `CvRequestSerializer` | `feat/cv-analysis` |
| 50 | Backend : prompt analyse dans `cv_agent.py` — points forts + recommandations | `feat/cv-analysis` |
| 51 | Backend : endpoint `/api/agents/cv/` gère les deux modes | `feat/cv-analysis` |
| 52 | Frontend : toggle Adapter / Analyser sur `CvView.vue` | `feat/cv-analysis` |
| 53 | Frontend : `AnalysisCard.vue` — affichage points forts et recommandations | `feat/cv-analysis` |
| 54 | Frontend : `api.js` — passer le paramètre `mode` dans `streamCv()` | `feat/cv-analysis` |

---

## Backlog (plus tard)

- `feat/authentication` — login/register utilisateur (Django auth intégré)
- `feat/e2e-tests` — tests Playwright ou Cypress
