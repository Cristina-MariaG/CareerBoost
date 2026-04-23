import anthropic
from django.conf import settings


class ClaudeError(Exception):
    pass


def stream(system_prompt: str, user_message: str, cache_system: bool = False):
    """
    Streams Claude's response token by token.
    Yields text chunks as they arrive.
    cache_system=True activates prompt caching on the system prompt (useful for long contexts).
    """
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    system = _build_system(system_prompt, cache_system)

    try:
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            for text in stream.text_stream:
                yield text

    except anthropic.AuthenticationError:
        raise ClaudeError("Clé API Anthropic invalide.")
    except anthropic.RateLimitError:
        raise ClaudeError("Limite de taux Anthropic atteinte. Réessaie dans quelques secondes.")
    except anthropic.APITimeoutError:
        raise ClaudeError("Timeout — Claude n'a pas répondu à temps.")
    except anthropic.APIError as e:
        raise ClaudeError(f"Erreur API Anthropic : {e}")


def _build_system(system_prompt: str, cache: bool) -> list:
    block = {"type": "text", "text": system_prompt}
    if cache:
        block["cache_control"] = {"type": "ephemeral"}
    return [block]
