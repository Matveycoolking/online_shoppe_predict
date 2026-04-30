"""Model evaluation helpers."""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def _get_positive_class_scores(model: Any, X_test: Any) -> np.ndarray:
    """Return scores for ROC-AUC using predict_proba or decision_function."""
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X_test)
        return probabilities[:, 1]

    if hasattr(model, "decision_function"):
        scores = model.decision_function(X_test)
        return np.asarray(scores)

    raise AttributeError("Model does not support predict_proba or decision_function.")


def evaluate_model(model: Any, X_test: Any, y_test: Any) -> dict[str, Any]:
    """Evaluate a fitted model on test data."""
    y_pred = model.predict(X_test)
    y_score = _get_positive_class_scores(model, X_test)
    matrix = confusion_matrix(y_test, y_pred)

    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_score),
        "confusion_matrix": matrix.tolist(),
        "classification_report": classification_report(
            y_test,
            y_pred,
            zero_division=0,
            output_dict=True,
        ),
    }
