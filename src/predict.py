"""Prediction helpers for the saved purchase intention pipeline."""

from __future__ import annotations

from typing import Any

import joblib
import numpy as np
import pandas as pd

from src.config import BEST_MODEL_PATH


def load_model() -> Any:
    """Load the saved sklearn-compatible pipeline."""
    if not BEST_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file was not found: {BEST_MODEL_PATH}. "
            "Run `python -m src.train` first."
        )
    return joblib.load(BEST_MODEL_PATH)


def _positive_probability(model: Any, data: pd.DataFrame) -> float:
    """Return purchase probability from predict_proba or a decision score."""
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(data)
        return float(probabilities[0][1])

    if hasattr(model, "decision_function"):
        score = float(np.ravel(model.decision_function(data))[0])
        return float(1 / (1 + np.exp(-score)))

    raise AttributeError("Loaded model does not support probability estimation.")


def predict_single(input_data: dict[str, Any]) -> dict[str, Any]:
    """Predict purchase intention for one raw session dictionary."""
    model = load_model()
    input_frame = pd.DataFrame([input_data])

    prediction = bool(model.predict(input_frame)[0])
    purchase_probability = _positive_probability(model, input_frame)
    prediction_label = "Покупка вероятна" if prediction else "Покупка маловероятна"

    return {
        "prediction": prediction,
        "prediction_label": prediction_label,
        "purchase_probability": round(purchase_probability, 4),
    }
