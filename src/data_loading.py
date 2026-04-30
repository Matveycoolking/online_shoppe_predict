"""Utilities for loading and validating the shopper intention dataset."""

from pathlib import Path

import pandas as pd

from src.config import DATA_PATH, EXPECTED_COLUMNS


def validate_columns(df: pd.DataFrame) -> None:
    """Validate that all required columns are present in the dataset."""
    missing_columns = [column for column in EXPECTED_COLUMNS if column not in df.columns]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Dataset is missing required columns: {missing}")


def load_data(path: str | Path | None = None) -> pd.DataFrame:
    """Load the dataset from CSV and validate its columns."""
    data_path = Path(path) if path is not None else DATA_PATH

    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset file was not found: {data_path}. "
            "Place data.csv into the data/ directory."
        )

    df = pd.read_csv(data_path)
    validate_columns(df)
    return df
