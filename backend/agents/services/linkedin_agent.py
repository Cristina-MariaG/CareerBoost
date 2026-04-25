from .claude_client import stream, ClaudeError

TONES = {
    "professionnel": "Écris de manière professionnelle et sobre. Phrases courtes, vocabulaire précis, pas d'émojis. Adapté à un cadre ou recruteur.",
    "storytelling": "Écris comme une histoire personnelle et engageante. Commence par une accroche forte, crée de l'émotion, conclus avec une leçon ou un appel à l'action.",
    "technique": "Écris pour un public technique. Mets en avant les détails concrets : stack, architecture, décisions techniques. Pas de flou.",
}

SYSTEM_PROMPT = """Tu es un expert en personal branding LinkedIn.
Tu génères des posts LinkedIn percutants à partir d'une description fournie par l'utilisateur.
Tu respectes scrupuleusement le ton demandé.
Tu écris uniquement en français.
Tu retournes uniquement le post, sans commentaire ni explication."""


def generate(description: str, tone: str):
    """
    Yields a LinkedIn post token by token.
    tone must be one of: professionnel, storytelling, technique.
    """
    if tone not in TONES:
        raise ClaudeError(f"Ton invalide : '{tone}'. Choix possibles : {', '.join(TONES)}")

    user_message = f"""Ton demandé : {tone}
Consigne de ton : {TONES[tone]}

Description fournie par l'utilisateur :
{description}

Génère le post LinkedIn."""

    yield from stream(SYSTEM_PROMPT, user_message)
