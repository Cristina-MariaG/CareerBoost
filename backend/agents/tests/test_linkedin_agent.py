import json
import uuid
from unittest.mock import patch
from django.test import TestCase, Client
from agents.models import Session, GenerationHistory


class LinkedInAgentTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.session_id = str(uuid.uuid4())
        self.valid_payload = {
            "description": "J'ai lancé un projet Django avec Vue.js et Claude.",
            "tone": "professionnel",
            "session_id": self.session_id,
        }

    def _post(self, payload):
        return self.client.post(
            "/api/agents/linkedin/",
            data=json.dumps(payload),
            content_type="application/json",
        )

    @patch("agents.views.linkedin_agent_generate")
    def test_returns_sse_stream(self, mock_generate):
        mock_generate.return_value = iter(["Bonjour", " LinkedIn"])
        response = self._post(self.valid_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/event-stream")

    @patch("agents.views.linkedin_agent_generate")
    def test_stream_contains_tokens(self, mock_generate):
        mock_generate.return_value = iter(["Hello", " world"])
        response = self._post(self.valid_payload)
        content = b"".join(response.streaming_content).decode()
        self.assertIn('"text": "Hello"', content)
        self.assertIn('"text": " world"', content)
        self.assertIn("[DONE]", content)

    @patch("agents.views.linkedin_agent_generate")
    def test_saves_history_after_stream(self, mock_generate):
        mock_generate.return_value = iter(["Super post"])
        response = self._post(self.valid_payload)
        b"".join(response.streaming_content)  # consomme le stream pour déclencher la sauvegarde
        self.assertEqual(GenerationHistory.objects.count(), 1)
        entry = GenerationHistory.objects.first()
        self.assertEqual(entry.agent, "linkedin")
        self.assertEqual(entry.output, "Super post")

    @patch("agents.views.linkedin_agent_generate")
    def test_creates_session_if_not_exists(self, mock_generate):
        mock_generate.return_value = iter(["ok"])
        self._post(self.valid_payload)
        self.assertTrue(Session.objects.filter(id=self.session_id).exists())

    def test_returns_400_on_invalid_tone(self):
        payload = {**self.valid_payload, "tone": "agressif"}
        response = self._post(payload)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_on_short_description(self):
        payload = {**self.valid_payload, "description": "Court"}
        response = self._post(payload)
        self.assertEqual(response.status_code, 400)

    def test_returns_400_on_missing_field(self):
        payload = {"description": "Une description valide pour le test.", "tone": "professionnel"}
        response = self._post(payload)
        self.assertEqual(response.status_code, 400)
