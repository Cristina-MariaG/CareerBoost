import pdfplumber
from io import BytesIO

from .claude_client import stream, ClaudeError

SYSTEM_PROMPT = """Tu es un expert en recrutement et en rédaction de CV et lettres de motivation.
Tu adaptes les documents d'un candidat à une offre d'emploi spécifique.
Tu mets en avant les compétences et expériences les plus pertinentes pour le poste.
Tu respectes scrupuleusement la structure demandée dans le message utilisateur.
Tu écris uniquement en français.
Tu retournes uniquement le contenu adapté, sans commentaire ni explication."""


def extract_text_from_pdf(file_bytes: bytes) -> str:
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    text = "\n\n".join(pages).strip()
    if not text:
        raise ClaudeError("Le PDF ne contient pas de texte extractible.")
    return text


def generate(job_offer: str, cv_text: str, cover_letter_text: str = ""):
    """
    Yields adapted CV (+ cover letter if provided) token by token.
    cache_system=True because the system prompt is reused across requests.
    """
    if cover_letter_text:
        task = """Adapte le CV et la lettre de motivation à cette offre d'emploi.

Pour la lettre de motivation, respecte impérativement cette structure en 4 parties :
1. Premier paragraphe : présentation du candidat (qui je suis, mon parcours en une phrase).
2. Deuxième paragraphe : pourquoi cette entreprise — montrer que tu la connais, ce qui t'attire spécifiquement dans ses valeurs, son secteur ou ses projets.
3. Troisième paragraphe : ce que le candidat peut apporter à l'entreprise via ce poste — compétences concrètes, réalisations pertinentes, valeur ajoutée.
4. Phrase de clôture élégante et professionnelle (une seule phrase, formule de politesse incluse).

Structure ta réponse ainsi :
## CV adapté
[CV adapté ici]

## Lettre de motivation adaptée
[Lettre de motivation adaptée ici]"""
    else:
        task = """Adapte le CV à cette offre d'emploi.

Structure ta réponse ainsi :
## CV adapté
[CV adapté ici]"""

    lm_section = f"\n\nLettre de motivation actuelle :\n{cover_letter_text}" if cover_letter_text else ""

    user_message = f"""Offre d'emploi :
{job_offer}

CV actuel :
{cv_text}{lm_section}

{task}"""

    yield from stream(SYSTEM_PROMPT, user_message, cache_system=True)


SYSTEM_PROMPT_ANALYZE = """Tu es un expert en recrutement avec 15 ans d'expérience.
Tu analyses des CV par rapport à des offres d'emploi et fournis des retours actionnables.
Tu écris uniquement en français.
Tu retournes uniquement l'analyse structurée, sans commentaire introductif."""


def analyze(job_offer: str, cv_text: str, cover_letter_text: str = ""):
    lm_section = f"\n\nLettre de motivation :\n{cover_letter_text}" if cover_letter_text else ""

    user_message = f"""Offre d'emploi :
{job_offer}

CV du candidat :
{cv_text}{lm_section}

Analyse ce CV par rapport à l'offre et structure ta réponse ainsi :

## Points forts
Liste les 4 à 6 points forts du candidat pour ce poste.

## Points à améliorer
Liste les 3 à 5 points faibles ou manquants par rapport aux exigences de l'offre.

## Recommandations concrètes
Donne 4 à 6 recommandations précises et actionnables pour améliorer le CV.

## Score d'adéquation
Donne un score sur 10 avec une justification en une phrase."""

    yield from stream(SYSTEM_PROMPT_ANALYZE, user_message, cache_system=True)
