"""Train baseline and tree-based models for purchase intention prediction."""

from __future__ import annotations

import json
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline

from src.config import (
    BEST_MODEL_PATH,
    MODEL_METADATA_PATH,
    MODELS_DIR,
    RANDOM_STATE,
    REPORTS_DIR,
    TARGET_COLUMN,
    TEST_SIZE,
)
from src.data_loading import load_data
from src.evaluate import evaluate_model
from src.preprocessing import (
    CATEGORICAL_FEATURES,
    ENGINEERED_NUMERIC_FEATURES,
    NUMERIC_FEATURES,
    build_full_preprocessor,
)


def prepare_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Split the dataframe into features and binary target."""
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN].astype(int)
    return X, y


def build_models() -> dict[str, Any]:
    """Create model instances used in the experiment."""
    models: dict[str, Any] = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
    }

    try:
        from catboost import CatBoostClassifier

        models["CatBoost"] = CatBoostClassifier(
            iterations=500,
            learning_rate=0.05,
            depth=6,
            loss_function="Logloss",
            eval_metric="F1",
            random_seed=RANDOM_STATE,
            verbose=False,
        )
    except ImportError:
        models["HistGradientBoosting"] = HistGradientBoostingClassifier(
            random_state=RANDOM_STATE,
        )

    return models


def build_tuned_random_forest(X_train: pd.DataFrame, y_train: pd.Series) -> Pipeline:
    """Tune Random Forest with a small randomized search."""
    pipeline = Pipeline(
        steps=[
            ("preprocessor", build_full_preprocessor()),
            (
                "model",
                RandomForestClassifier(
                    class_weight="balanced",
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    param_distributions = {
        "model__n_estimators": [200, 300, 500],
        "model__max_depth": [None, 6, 10, 14],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
        "model__max_features": ["sqrt", "log2", None],
    }

    cv = StratifiedKFold(
        n_splits=3,
        shuffle=True,
        random_state=RANDOM_STATE,
    )
    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=param_distributions,
        n_iter=8,
        scoring="f1",
        cv=cv,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbose=1,
    )
    search.fit(X_train, y_train)
    print(f"Best Random Forest Tuned params: {search.best_params_}")
    print(f"Best Random Forest Tuned CV F1: {search.best_score_:.4f}")
    return search.best_estimator_


def _build_pipeline(model: Any) -> Pipeline:
    """Wrap preprocessing and estimator into one sklearn Pipeline."""
    return Pipeline(
        steps=[
            ("preprocessor", build_full_preprocessor()),
            ("model", model),
        ]
    )


def _flatten_metrics(model_name: str, metrics: dict[str, Any]) -> dict[str, Any]:
    """Prepare metrics for saving as a CSV row."""
    confusion = metrics["confusion_matrix"]
    return {
        "model": model_name,
        "accuracy": metrics["accuracy"],
        "precision": metrics["precision"],
        "recall": metrics["recall"],
        "f1": metrics["f1"],
        "roc_auc": metrics["roc_auc"],
        "tn": confusion[0][0],
        "fp": confusion[0][1],
        "fn": confusion[1][0],
        "tp": confusion[1][1],
        "confusion_matrix": json.dumps(confusion),
    }


def _compact_metrics(metrics: dict[str, Any]) -> dict[str, float]:
    """Return JSON-friendly core metrics."""
    return {
        "accuracy": float(metrics["accuracy"]),
        "precision": float(metrics["precision"]),
        "recall": float(metrics["recall"]),
        "f1": float(metrics["f1"]),
        "roc_auc": float(metrics["roc_auc"]),
    }


def _save_best_model(
    trained_models: dict[str, Pipeline],
    metrics_by_model: dict[str, dict[str, Any]],
    comparison: pd.DataFrame,
) -> tuple[str, Pipeline]:
    """Save the best model by F1-score and write metadata."""
    best_model_name = str(comparison.iloc[0]["model"])
    best_model = trained_models[best_model_name]
    best_metrics = metrics_by_model[best_model_name]

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, BEST_MODEL_PATH)

    metadata = {
        "best_model_name": best_model_name,
        "selection_metric": "f1",
        "metrics": _compact_metrics(best_metrics),
        "features": {
            "numeric": NUMERIC_FEATURES,
            "categorical": CATEGORICAL_FEATURES,
            "engineered": ENGINEERED_NUMERIC_FEATURES,
        },
        "target": TARGET_COLUMN,
    }

    MODEL_METADATA_PATH.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return best_model_name, best_model


def train_models() -> pd.DataFrame:
    """Train all models, evaluate them and save the best pipeline."""
    df = load_data()
    X, y = prepare_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    rows: list[dict[str, Any]] = []
    trained_models: dict[str, Pipeline] = {}
    metrics_by_model: dict[str, dict[str, Any]] = {}

    for model_name, model in build_models().items():
        pipeline = _build_pipeline(model)
        pipeline.fit(X_train, y_train)
        metrics = evaluate_model(pipeline, X_test, y_test)
        trained_models[model_name] = pipeline
        metrics_by_model[model_name] = metrics
        rows.append(_flatten_metrics(model_name, metrics))

    tuned_rf = build_tuned_random_forest(X_train, y_train)
    tuned_rf_metrics = evaluate_model(tuned_rf, X_test, y_test)
    trained_models["Random Forest Tuned"] = tuned_rf
    metrics_by_model["Random Forest Tuned"] = tuned_rf_metrics
    rows.append(_flatten_metrics("Random Forest Tuned", tuned_rf_metrics))

    comparison = pd.DataFrame(rows).sort_values(
        by=["f1", "roc_auc"],
        ascending=False,
    )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(REPORTS_DIR / "model_comparison.csv", index=False)
    best_model_name, _ = _save_best_model(trained_models, metrics_by_model, comparison)
    print(f"Best model saved: {best_model_name} -> {BEST_MODEL_PATH}")
    return comparison


if __name__ == "__main__":
    results = train_models()
    print(results.to_string(index=False))
