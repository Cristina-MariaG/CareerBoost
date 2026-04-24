from unittest.mock import MagicMock, patch
from django.test import TestCase
from agents.services.claude_client import stream, ClaudeError
import anthropic


def _mock_stream(tokens):
    mock = MagicMock()
    mock.__enter__ = MagicMock(return_value=mock)
    mock.__exit__ = MagicMock(return_value=False)
    mock.text_stream = iter(tokens)
    return mock


class ClaudeClientTest(TestCase):

    @patch("agents.services.claude_client.anthropic.Anthropic")
    def test_stream_yields_text(self, mock_anthropic):
        mock_anthropic.return_value.messages.stream.return_value = _mock_stream(["Bonjour", " le", " monde"])
        result = list(stream("Tu es un assistant.", "Dis bonjour."))
        self.assertEqual(result, ["Bonjour", " le", " monde"])

    @patch("agents.services.claude_client.anthropic.Anthropic")
    def test_stream_raises_on_empty_response(self, mock_anthropic):
        mock_anthropic.return_value.messages.stream.return_value = _mock_stream([])
        with self.assertRaises(ClaudeError):
            list(stream("system", "user"))

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
    def test_stream_raises_on_timeout(self, mock_anthropic):
        mock_anthropic.return_value.messages.stream.side_effect = anthropic.APITimeoutError(
            request=MagicMock()
        )
        with self.assertRaises(ClaudeError):
            list(stream("system", "user"))

    @patch("agents.services.claude_client.anthropic.Anthropic")
    def test_cache_control_added_when_requested(self, mock_anthropic):
        mock_anthropic.return_value.messages.stream.return_value = _mock_stream(["ok"])
        list(stream("system prompt", "user message", cache_system=True))
        call_kwargs = mock_anthropic.return_value.messages.stream.call_args[1]
        self.assertEqual(call_kwargs["system"][0]["cache_control"], {"type": "ephemeral"})

    @patch("agents.services.claude_client.anthropic.Anthropic")
    def test_cache_control_absent_when_not_requested(self, mock_anthropic):
        mock_anthropic.return_value.messages.stream.return_value = _mock_stream(["ok"])
        list(stream("system prompt", "user message", cache_system=False))
        call_kwargs = mock_anthropic.return_value.messages.stream.call_args[1]
        self.assertNotIn("cache_control", call_kwargs["system"][0])
