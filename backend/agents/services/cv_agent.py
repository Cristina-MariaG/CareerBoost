import pdfplumber
from io import BytesIO

from .claude_client import stream, ClaudeError

SYSTEM_PROMPT = """Tu es un expert en recrutement et en rédaction de CV et lettres de motivation.
Tu adaptes le CV et la lettre de motivation d'un candidat à une offre d'emploi spécifique.
Tu mets en avant les compétences et expériences les plus pertinentes pour le poste.
Tu écris uniquement en français.
Tu retournes uniquement le contenu adapté, sans commentaire ni explication."""


def extract_text_from_pdf(file_bytes: bytes) -> str:
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    text = "\n\n".join(pages).strip()
    if not text:
        raise ClaudeError("Le PDF ne contient pas de texte extractible.")
    return text


def generate(job_offer: str, cv_text: str, cover_letter_text: str):
    """
    Yields adapted CV + cover letter token by token.
    cache_system=True because the system prompt is reused across requests.
    """
    user_message = f"""Offre d'emploi :
{job_offer}

CV actuel :
{cv_text}

Lettre de motivation actuelle :
{cover_letter_text}

Adapte le CV et la lettre de motivation à cette offre d'emploi."""

    yield from stream(SYSTEM_PROMPT, user_message, cache_system=True)
