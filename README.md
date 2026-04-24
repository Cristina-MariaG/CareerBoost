# CareerBoost

Application web avec deux agents IA propulsés par Claude (Anthropic) :

- **Agent LinkedIn** — génère un post LinkedIn optimisé à partir d'une description, avec choix de ton (professionnel, storytelling, technique)
- **Agent CV & LM** — adapte un CV et une lettre de motivation à une offre d'emploi (upload PDF)

**Stack :** Django 5 + DRF · Vue.js 3 · PostgreSQL · Docker · Anthropic SDK

---

## Prérequis

- [Docker](https://www.docker.com/) installé
- Une clé API Anthropic ([console.anthropic.com](https://console.anthropic.com))

---

## Premier démarrage

```bash
# 1. Copier le fichier d'environnement et renseigner la clé API
cp .env.example .env
# Ouvrir .env et remplir ANTHROPIC_API_KEY

# 2. Construire et démarrer les conteneurs
docker compose up --build

# 3. Dans un autre terminal — lancer les migrations (une seule fois)
docker compose exec backend python manage.py migrate

# 4. Vérifier que le backend répond
curl http://localhost:8000/api/health/
# → {"status": "ok"}
```

L'application est disponible sur `http://localhost:5173`.

---

## Démarrages suivants

```bash
docker compose up
```

---

## Commandes utiles

```bash
# Créer les migrations après modification des models
docker compose exec backend python manage.py makemigrations

# Appliquer les migrations
docker compose exec backend python manage.py migrate

# Accéder au shell Django
docker compose exec backend python manage.py shell

# Logs d'un service spécifique
docker compose logs -f backend
docker compose logs -f frontend

# Stopper et supprimer les conteneurs
docker compose down

# Stopper et supprimer aussi les volumes (repart de zéro)
docker compose down -v
```

---

## Structure

```
backend/        Django 5 + DRF + agents IA
frontend/       Vue.js 3 + Vite
docker-compose.yml
```

Voir [ROADMAP.md](ROADMAP.md) pour l'avancement du projet.
