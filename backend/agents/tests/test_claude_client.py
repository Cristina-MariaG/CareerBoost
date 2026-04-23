from unittest.mock import MagicMock, patch
from django.test import TestCase
from agents.services.claude_client import stream, ClaudeError
import anthropic


class ClaudeClientTest(TestCase):

    @patch("agents.services.claude_client.anthropic.Anthropic")
    def test_stream_yields_text(self, mock_anthropic):
        mock_stream = MagicMock()
        mock_stream.__enter__ = MagicMock(return_value=mock_stream)
        mock_stream.__exit__ = MagicMock(return_value=False)
        mock_stream.text_stream = iter(["Bonjour", " le", " monde"])
        mock_anthropic.return_value.messages.stream.return_value = mock_stream

        result = list(stream("Tu es un assistant.", "Dis bonjour."))
        self.assertEqual(result, ["Bonjour", " le", " monde"])

    @patch("agents.services.claude_client.anthropic.Anthropic")
    def test_stream_raises_on_auth_error(self, mock_anthropic):
        mock_anthropic.return_value.messages.stream.side_effect = anthropic.AuthenticationError(
            message="invalid key", response=MagicMock(), body={}
        )
        with self.assertRaises(ClaudeError):
            list(stream("system", "user"))

    @patch("agents.services.claude_client.anthropic.Anthropic")
    def test_stream_raises_on_rate_limit(self, mock_anthropic):
        mock_anthropic.return_value.messages.stream.side_effect = anthropic.RateLimitError(
            message="rate limit", response=MagicMock(), body={}
        )
        with self.assertRaises(ClaudeError):
            list(stream("system", "user"))

    @patch("agents.services.claude_client.anthropic.Anthropic")
    def test_cache_control_added_when_requested(self, mock_anthropic):
        mock_stream = MagicMock()
        mock_stream.__enter__ = MagicMock(return_value=mock_stream)
        mock_stream.__exit__ = MagicMock(return_value=False)
        mock_stream.text_stream = iter([])
        mock_anthropic.return_value.messages.stream.return_value = mock_stream

        list(stream("system prompt", "user message", cache_system=True))

        call_kwargs = mock_anthropic.return_value.messages.stream.call_args[1]
        self.assertEqual(call_kwargs["system"][0]["cache_control"], {"type": "ephemeral"})
