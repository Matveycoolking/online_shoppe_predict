"""Preprocessing pipeline for the shopper intention dataset."""

from __future__ import annotations

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

NUMERIC_FEATURES = [
    "Administrative",
    "Administrative_Duration",
    "Informational",
    "Informational_Duration",
    "ProductRelated",
    "ProductRelated_Duration",
    "BounceRates",
    "ExitRates",
    "PageValues",
    "SpecialDay",
    "TotalPages",
    "TotalDuration",
    "ProductPagesShare",
    "AvgProductDuration",
    "HasPageValue",
]

BASE_NUMERIC_FEATURES = [
    "Administrative",
    "Administrative_Duration",
    "Informational",
    "Informational_Duration",
    "ProductRelated",
    "ProductRelated_Duration",
    "BounceRates",
    "ExitRates",
    "PageValues",
    "SpecialDay",
]

ENGINEERED_NUMERIC_FEATURES = [
    "TotalPages",
    "TotalDuration",
    "ProductPagesShare",
    "AvgProductDuration",
    "HasPageValue",
]

CATEGORICAL_FEATURES = [
    "Month",
    "OperatingSystems",
    "Browser",
    "Region",
    "TrafficType",
    "VisitorType",
    "Weekend",
]


class FeatureEngineer(BaseEstimator, TransformerMixin):
    """Add behavior-based features while keeping raw input compatibility."""

    def fit(self, X: pd.DataFrame, y: pd.Series | None = None) -> "FeatureEngineer":
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        frame = X.copy()
        total_pages = (
            frame["Administrative"]
            + frame["Informational"]
            + frame["ProductRelated"]
        )
        total_duration = (
            frame["Administrative_Duration"]
            + frame["Informational_Duration"]
            + frame["ProductRelated_Duration"]
        )

        frame["TotalPages"] = total_pages
        frame["TotalDuration"] = total_duration
        frame["ProductPagesShare"] = (frame["ProductRelated"] / total_pages).where(
            total_pages > 0,
            0.0,
        )
        frame["AvgProductDuration"] = (
            frame["ProductRelated_Duration"] / frame["ProductRelated"]
        ).where(frame["ProductRelated"] > 0, 0.0)
        frame["HasPageValue"] = (frame["PageValues"] > 0).astype(int)
        return frame


def _build_one_hot_encoder() -> OneHotEncoder:
    """Create OneHotEncoder with compatibility for different sklearn versions."""
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def _cast_categorical_to_string(data):
    """Cast non-missing categorical values to string and preserve missing values."""
    frame = pd.DataFrame(data).copy()
    return frame.map(lambda value: value if pd.isna(value) else str(value))


def build_preprocessor() -> ColumnTransformer:
    """Build a ColumnTransformer for numeric and categorical features."""
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            (
                "to_string",
                FunctionTransformer(
                    _cast_categorical_to_string,
                    feature_names_out="one-to-one",
                ),
            ),
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", _build_one_hot_encoder()),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )


def build_full_preprocessor() -> Pipeline:
    """Build feature engineering plus preprocessing as one pipeline step."""
    return Pipeline(
        steps=[
            ("feature_engineering", FeatureEngineer()),
            ("column_transformer", build_preprocessor()),
        ]
    )
