"""FastAPI entry point for the local BERT hotel-review demo."""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel

from src.predict import predict_bert

APP_DIR = Path(__file__).resolve().parent
MAX_DEMO_CHARACTERS = 5_000

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="BERT Sentiment Analysis Demo", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")
templates = Jinja2Templates(directory=APP_DIR / "templates")


class PredictionRequest(BaseModel):
    text: str


class PredictionResponse(BaseModel):
    label: str
    confidence: float
    probabilities: dict[str, float]


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    """Serve the single-page presentation interface."""
    return templates.TemplateResponse(request, "index.html")


@app.post("/api/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest) -> PredictionResponse:
    """Run the canonical BERT inference function and return its probabilities."""
    text = payload.text.strip()
    if not text:
        raise HTTPException(
            status_code=422,
            detail="Please enter a hotel review before analyzing.",
        )
    if len(text) > MAX_DEMO_CHARACTERS:
        raise HTTPException(
            status_code=422,
            detail="Please keep the local demo input within 5,000 characters.",
        )

    try:
        result = predict_bert(text)
    except OSError as exc:
        logger.warning("BERT model artifact is unavailable: %s", exc)
        raise HTTPException(
            status_code=503,
            detail=(
                "Model artifact not found. Please place the trained BERT model "
                "in the expected artifacts/model directory."
            ),
        ) from exc
    except Exception:
        logger.exception("BERT prediction failed")
        raise HTTPException(
            status_code=500,
            detail="Prediction could not be completed. Please try again.",
        )

    return PredictionResponse(
        label=result["label"].lower(),
        confidence=result["confidence"],
        probabilities={
            "negative": result["prob_negative"],
            "positive": result["prob_positive"],
        },
    )
