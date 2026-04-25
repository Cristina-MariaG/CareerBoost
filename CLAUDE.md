# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

CareerBoost — Django REST Framework backend + Vue.js 3 frontend with two Claude-powered AI agents:
- **Agent LinkedIn** : génère un post LinkedIn à partir d'une description, avec choix de ton (professionnel / storytelling / technique)
- **Agent CV & LM** : adapte un CV et une lettre de motivation à une offre d'emploi (input : texte offre + PDF upload)

## Stack

- Python 3.13 / Django 5 / Django REST Framework
- Anthropic SDK — modèle **`claude-sonnet-4-6`** (pas `claude-sonnet-4-20250514` qui est invalide)
- Vue.js 3 + Vite + Vue Router + Axios
- PostgreSQL (dev + prod via docker-compose)
- Docker + docker-compose

## Commands

```bash
# Lancer tout l'environnement
docker compose up

# Backend seul (depuis backend/)
python manage.py migrate
python manage.py runserver

# Frontend seul (depuis frontend/)
npm install
npm run dev

# Tests backend
python manage.py test agents

# Créer les migrations après modification des models
python manage.py makemigrations
```

## Architecture

```
backend/
├── config/          # settings.py, urls.py, wsgi.py — projet Django
├── agents/          # app principale
│   ├── services/
│   │   ├── claude_client.py    # wrapper SDK Anthropic (shared par les 2 agents)
│   │   ├── linkedin_agent.py   # prompt engineering LinkedIn (3 tons)
│   │   └── cv_agent.py         # prompt engineering CV + parsing PDF
│   ├── tests/
│   │   ├── test_claude_client.py   # 7 tests : streaming, erreurs, caching
│   │   └── test_linkedin_agent.py  # 7 tests : endpoint SSE, serializer, historique
│   ├── models.py       # Session (UUID anonyme), GenerationHistory
│   ├── serializers.py  # LinkedInRequestSerializer (validation description, ton, session_id)
│   ├── views.py        # endpoints DRF + StreamingHttpResponse (SSE)
│   └── urls.py         # GET /api/health/, POST /api/agents/linkedin/
frontend/
├── src/
│   ├── services/api.js          # instance Axios, baseURL=/api
│   ├── router/index.js          # routes /linkedin et /cv
│   ├── views/                   # LinkedinView.vue, CvView.vue
│   └── components/              # PostResult.vue, FileUpload.vue, ResultCard.vue
```

### Flux de données

```
Vue (EventSource) → POST /api/agents/linkedin/ ou /api/agents/cv/
  → LinkedInRequestSerializer (validation)
  → DRF view → agent service → claude_client.py (streaming)
  → StreamingHttpResponse (SSE) → Vue affiche token par token
  → GenerationHistory sauvegardé en base après le stream
```

### Endpoints disponibles

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/health/` | Healthcheck backend |
| POST | `/api/agents/linkedin/` | Génère un post LinkedIn (SSE) |

## Décisions clés

**Streaming SSE** — les réponses Claude sont streamées token par token via `StreamingHttpResponse`. Ne pas remplacer par une réponse JSON bloquante sans raison valable (UX dégradée sur 10-15s).

**Prompt caching** — activé dans `claude_client.py` pour réduire les coûts sur l'agent CV (contexte long : offre + CV + LM).

**Sessions anonymes** — pas d'auth pour l'instant. Les sessions utilisent un UUID stocké côté client. L'auth sera ajoutée dans une branche `feat/authentication` dédiée.

**Format de sortie** — Markdown. Claude retourne du Markdown, le frontend le rend.

**PDF** — supprimés immédiatement après extraction du texte (RGPD + espace). Ne pas persister les fichiers uploadés.

**Base de données** — PostgreSQL dès le dev (pas de SQLite). Credentials dans `.env`.

## Variables d'environnement

Voir `.env.example`. Variables critiques :

| Variable | Usage |
|----------|-------|
| `ANTHROPIC_API_KEY` | Clé API Anthropic |
| `DJANGO_SECRET_KEY` | Secret Django |
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | Credentials PostgreSQL |
| `CORS_ALLOWED_ORIGINS` | Ex: `http://localhost:5173` |
| `BACKEND_URL` | Cible du proxy Vite (docker: `http://backend:8000`) |

## Conventions Git

- Branches : `feat/`, `fix/`, `chore/` — une branche = une PR
- Merge sur `develop`, puis `main` quand la feature est testée
- Ordre des branches : `chore/project-init` → `feat/claude-client` → `feat/linkedin-agent-api` → `feat/linkedin-agent-ui` → `feat/pdf-handling` → `feat/cv-agent-api` → `feat/cv-agent-ui` → `chore/docker-prod`
