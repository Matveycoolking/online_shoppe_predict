"""FastAPI application for purchase intention prediction."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import PredictionResponse, ShopperSession
from src.config import BEST_MODEL_PATH
from src.predict import load_model, predict_single

app = FastAPI(
    title="Online Shopper Purchase Intention API",
    description="API for predicting whether an online shopping session will end with a purchase.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    """Return basic project information."""
    return {
        "project": "Online Shopper Purchase Intention",
        "task": "Binary classification of user sessions",
        "target": "Revenue",
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict[str, bool | str]:
    """Return service status and model availability."""
    model_loaded = False
    if BEST_MODEL_PATH.exists():
        try:
            load_model()
            model_loaded = True
        except Exception:
            model_loaded = False

    return {
        "status": "ok",
        "model_loaded": model_loaded,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(session: ShopperSession) -> PredictionResponse:
    """Predict purchase intention for one shopper session."""
    try:
        result = predict_single(session.model_dump())
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="Model file not found. Run `python -m src.train` first.",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Could not make prediction: {exc}",
        ) from exc

    return PredictionResponse(**result)
