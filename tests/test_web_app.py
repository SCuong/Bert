import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


class WebApplicationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_home_page_serves_the_sentiment_interface(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("BERT Sentiment Analysis", response.text)
        self.assertIn("Hotel Review Classification", response.text)
        self.assertIn("/static/css/style.css", response.text)

    def test_predict_rejects_blank_review(self):
        response = self.client.post("/api/predict", json={"text": "   "})

        self.assertEqual(response.status_code, 422)
        self.assertIn("Please enter a hotel review", response.json()["detail"])

    def test_predict_rejects_text_beyond_demo_request_limit(self):
        response = self.client.post("/api/predict", json={"text": "a" * 5001})

        self.assertEqual(response.status_code, 422)
        self.assertIn("5,000 characters", response.json()["detail"])

    @patch("app.main.predict_bert")
    def test_predict_returns_actual_bert_probabilities(self, predict_bert):
        predict_bert.return_value = {
            "label": "Positive",
            "confidence": 0.924,
            "prob_negative": 0.076,
            "prob_positive": 0.924,
        }

        response = self.client.post(
            "/api/predict",
            json={"text": "The room was clean and the staff were very friendly."},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "label": "positive",
                "confidence": 0.924,
                "probabilities": {"negative": 0.076, "positive": 0.924},
            },
        )
        predict_bert.assert_called_once_with(
            "The room was clean and the staff were very friendly."
        )

    @patch("app.main.predict_bert", side_effect=FileNotFoundError("model missing"))
    def test_predict_returns_safe_model_unavailable_error(self, _predict_bert):
        response = self.client.post("/api/predict", json={"text": "A review."})

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["detail"], "Model artifact not found. Please place the trained BERT model in the expected artifacts/model directory.")

    @patch("app.main.predict_bert", side_effect=OSError("unable to load model artifact"))
    def test_predict_returns_safe_error_for_unreadable_model_artifact(self, _predict_bert):
        response = self.client.post("/api/predict", json={"text": "A review."})

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["detail"], "Model artifact not found. Please place the trained BERT model in the expected artifacts/model directory.")


if __name__ == "__main__":
    unittest.main()
