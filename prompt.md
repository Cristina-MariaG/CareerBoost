Je veux créer une application web avec Django REST Framework (backend) et Vue.js (frontend) qui contient 2 agents IA propulsés par l'API Anthropic (Claude).
Agent 1 — LinkedIn Post Generator
L'utilisateur décrit son dernier travail ou projet, et l'agent génère un post LinkedIn optimisé, avec choix de ton (professionnel, storytelling, technique).
Agent 2 — CV & Lettre de motivation
L'utilisateur colle une offre d'emploi et uploade son CV et/ou sa lettre de motivation existants (PDF). L'agent génère un CV et une lettre de motivation adaptés à l'offre.
Structure du projet :
project/
├── backend/                  # Django + DRF
│   ├── config/               # Settings, urls, wsgi
│   ├── agents/               # App principale
│   │   ├── models.py         # Session, historique
│   │   ├── views.py          # Endpoints API
│   │   ├── serializers.py
│   │   ├── services/
│   │   │   ├── linkedin_agent.py
│   │   │   ├── cv_agent.py
│   │   │   └── claude_client.py
│   │   └── urls.py
│   ├── requirements.txt
│   └── manage.py
├── frontend/                 # Vue.js
│   ├── src/
│   │   ├── views/
│   │   │   ├── LinkedinView.vue
│   │   │   └── CvView.vue
│   │   ├── components/
│   │   │   ├── PostResult.vue
│   │   │   ├── FileUpload.vue
│   │   │   └── ResultCard.vue
│   │   ├── services/
│   │   │   └── api.js
│   │   └── router/
│   └── package.json
├── docker-compose.yml
└── README.md
Endpoints DRF :

POST /api/agents/linkedin/ — génère un post LinkedIn
POST /api/agents/cv/ — génère CV + LM à partir de l'offre + fichiers PDF uploadés

Stack :

Python 3.11+
Django 5 + Django REST Framework
Anthropic SDK (claude-sonnet-4-20250514)
Vue.js 3 + Vue Router + Axios
Docker + docker-compose pour lancer le tout

Important — méthode de travail :
On travaille étape par étape, dans l'ordre logique. Chaque étape doit être validée avant de passer à la suivante. On respecte les bonnes pratiques Git :

Une branche par fonctionnalité (feature/linkedin-agent, feature/cv-agent, feature/frontend-linkedin, etc.)
Des commits clairs et bien nommés (feat: add linkedin agent service, fix: cors configuration, chore: add docker-compose)
On merge sur main uniquement quand une feature est terminée et testée

Commence par initialiser le repo Git, créer la branche main, puis la structure du projet. Ensuite on avancera fonctionnalité par fonctionnalité.
