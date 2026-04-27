import io
import uuid
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from agents.models import Session, GenerationHistory
from agents.services.cv_agent import extract_text_from_pdf
from agents.services.claude_client import ClaudeError


def _make_pdf(text="Mon CV en Python"):
    # We mock pdfplumber.open instead to avoid needing a real PDF in tests.
    pass


class ExtractTextFromPdfTest(TestCase):

    @patch("agents.services.cv_agent.pdfplumber.open")
    def test_extracts_text_from_pages(self, mock_open):
        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = "Page 1 contenu"
        mock_page2 = MagicMock()
        mock_page2.extract_text.return_value = "Page 2 contenu"
        mock_open.return_value.__enter__.return_value.pages = [mock_page1, mock_page2]

        result = extract_text_from_pdf(b"fake-pdf-bytes")
        self.assertIn("Page 1 contenu", result)
        self.assertIn("Page 2 contenu", result)

    @patch("agents.services.cv_agent.pdfplumber.open")
    def test_raises_on_empty_pdf(self, mock_open):
        mock_page = MagicMock()
        mock_page.extract_text.return_value = None
        mock_open.return_value.__enter__.return_value.pages = [mock_page]

        with self.assertRaises(ClaudeError):
            extract_text_from_pdf(b"fake-pdf-bytes")

    @patch("agents.services.cv_agent.pdfplumber.open")
    def test_skips_none_pages(self, mock_open):
        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = None
        mock_page2 = MagicMock()
        mock_page2.extract_text.return_value = "Contenu valide"
        mock_open.return_value.__enter__.return_value.pages = [mock_page1, mock_page2]

        result = extract_text_from_pdf(b"fake-pdf-bytes")
        self.assertIn("Contenu valide", result)


class CvEndpointTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.session_id = str(uuid.uuid4())

    def _make_pdf_file(self, name="cv.pdf", content=b"fake-pdf"):
        return io.BytesIO(content), name

    def _post(self, job_offer, cv_bytes, cv_name="cv.pdf", cover_letter_bytes=None, cover_letter_name="lm.pdf"):
        data = {
            "job_offer": job_offer,
            "session_id": self.session_id,
            "cv": io.BytesIO(cv_bytes),
        }
        data["cv"].name = cv_name
        if cover_letter_bytes is not None:
            lm = io.BytesIO(cover_letter_bytes)
            lm.name = cover_letter_name
            data["cover_letter"] = lm
        return self.client.post("/api/agents/cv/", data=data, format="multipart")

    @patch("agents.views.cv_agent_generate")
    @patch("agents.views.extract_text_from_pdf")
    def test_returns_sse_stream(self, mock_extract, mock_generate):
        mock_extract.return_value = "Texte du CV"
        mock_generate.return_value = iter(["CV adapté"])
        response = self._post(
            job_offer="Développeur Python senior avec 5 ans d'expérience en Django.",
            cv_bytes=b"%PDF-fake",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/event-stream")

    @patch("agents.views.cv_agent_generate")
    @patch("agents.views.extract_text_from_pdf")
    def test_stream_contains_tokens(self, mock_extract, mock_generate):
        mock_extract.return_value = "Texte du CV"
        mock_generate.return_value = iter(["Bonjour", " CV"])
        response = self._post(
            job_offer="Développeur Python senior avec 5 ans d'expérience en Django.",
            cv_bytes=b"%PDF-fake",
        )
        content = b"".join(response.streaming_content).decode()
        self.assertIn('"text": "Bonjour"', content)
        self.assertIn("[DONE]", content)

    @patch("agents.views.cv_agent_generate")
    @patch("agents.views.extract_text_from_pdf")
    def test_saves_history_after_stream(self, mock_extract, mock_generate):
        mock_extract.return_value = "Texte du CV"
        mock_generate.return_value = iter(["CV généré"])
        response = self._post(
            job_offer="Développeur Python senior avec 5 ans d'expérience en Django.",
            cv_bytes=b"%PDF-fake",
        )
        b"".join(response.streaming_content)
        self.assertEqual(GenerationHistory.objects.count(), 1)
        entry = GenerationHistory.objects.first()
        self.assertEqual(entry.agent, "cv")
        self.assertEqual(entry.output, "CV généré")

    @patch("agents.views.cv_agent_generate")
    @patch("agents.views.extract_text_from_pdf")
    def test_creates_session_if_not_exists(self, mock_extract, mock_generate):
        mock_extract.return_value = "Texte du CV"
        mock_generate.return_value = iter(["ok"])
        self._post(
            job_offer="Développeur Python senior avec 5 ans d'expérience en Django.",
            cv_bytes=b"%PDF-fake",
        )
        self.assertTrue(Session.objects.filter(id=self.session_id).exists())

    def test_returns_400_on_non_pdf_cv(self):
        data = {
            "job_offer": "Développeur Python senior avec 5 ans d'expérience en Django.",
            "session_id": self.session_id,
        }
        f = io.BytesIO(b"not a pdf")
        f.name = "cv.docx"
        data["cv"] = f
        response = self.client.post("/api/agents/cv/", data=data, format="multipart")
        self.assertEqual(response.status_code, 400)

    def test_returns_400_on_short_job_offer(self):
        data = {
            "job_offer": "Trop court",
            "session_id": self.session_id,
        }
        f = io.BytesIO(b"fake-pdf")
        f.name = "cv.pdf"
        data["cv"] = f
        response = self.client.post("/api/agents/cv/", data=data, format="multipart")
        self.assertEqual(response.status_code, 400)

    def test_returns_400_on_missing_cv(self):
        data = {
            "job_offer": "Développeur Python senior avec 5 ans d'expérience en Django.",
            "session_id": self.session_id,
        }
        response = self.client.post("/api/agents/cv/", data=data, format="multipart")
        self.assertEqual(response.status_code, 400)
