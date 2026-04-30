"""Project configuration and shared paths."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
REPORTS_DIR = ROOT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
MODELS_DIR = ROOT_DIR / "models"

DATA_PATH = DATA_DIR / "data.csv"
BEST_MODEL_PATH = MODELS_DIR / "best_model.pkl"
MODEL_METADATA_PATH = MODELS_DIR / "metadata.json"

RANDOM_STATE = 42
TEST_SIZE = 0.2
TARGET_COLUMN = "Revenue"

EXPECTED_COLUMNS = [
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
    "Month",
    "OperatingSystems",
    "Browser",
    "Region",
    "TrafficType",
    "VisitorType",
    "Weekend",
    "Revenue",
]


def ensure_directories() -> None:
    """Create project output directories if they do not exist."""
    for directory in (DATA_DIR, REPORTS_DIR, FIGURES_DIR, MODELS_DIR):
        directory.mkdir(parents=True, exist_ok=True)


ensure_directories()
