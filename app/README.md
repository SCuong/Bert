# BERT Sentiment Analysis Demo

A lightweight local presentation interface for the hotel-review sentiment classifier.

## Run

From the repository root:

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Architecture

- `main.py` serves the Jinja2 page and exposes `POST /api/predict`.
- `templates/index.html` provides the single-page structure.
- `static/` contains dependency-free CSS and vanilla JavaScript.
- The endpoint calls `src.predict.predict_bert` directly, so the displayed label and probabilities are the canonical model output.

The model and tokenizer are cached by `src.predict`; they are not reloaded for every request. If the model artifact is unavailable, the interface returns a clear, non-technical error message.
