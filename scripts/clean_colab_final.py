from __future__ import annotations

import json
from pathlib import Path


PATHS = [
    Path(r"C:\Users\matve\Downloads\online_shopper_intention_colab_improved_clean.ipynb"),
    Path(r"C:\Users\matve\Desktop\InternetBying\notebooks\online_shopper_intention_colab_improved_clean.ipynb"),
]


def source(text: str) -> list[str]:
    return [line + "\n" for line in text.strip("\n").split("\n")]


def main() -> None:
    nb = json.loads(PATHS[0].read_text(encoding="utf-8"))
    cells = nb["cells"]

    # Remove unused artifact-saving imports.
    for cell in cells:
        if cell.get("cell_type") == "code" and "import joblib" in "".join(cell.get("source", [])):
            src = "".join(cell["source"])
            src = src.replace("import joblib\n", "")
            src = src.replace("from pathlib import Path\n", "")
            cell["source"] = source(src)
            break

    # Replace final best-model cell with an in-memory-only version.
    for cell in cells:
        src = "".join(cell.get("source", []))
        if cell.get("cell_type") == "code" and "joblib.dump(best_model" in src:
            cell["source"] = source(
                """
best_model_name = str(comparison.iloc[0]["model"])
best_model = trained_models[best_model_name]
best_metrics = metrics_by_model[best_model_name]

metadata = {
    "best_model_name": best_model_name,
    "selection_metric": "f1",
    "metrics": {
        "accuracy": float(best_metrics["accuracy"]),
        "precision": float(best_metrics["precision"]),
        "recall": float(best_metrics["recall"]),
        "f1": float(best_metrics["f1"]),
        "roc_auc": float(best_metrics["roc_auc"]),
    },
    "features": {
        "numeric": NUMERIC_FEATURES,
        "categorical": CATEGORICAL_FEATURES,
        "engineered": ENGINEERED_NUMERIC_FEATURES,
    },
    "target": TARGET_COLUMN,
}

print(f"Лучшая модель: {best_model_name}")
print(json.dumps(metadata, ensure_ascii=False, indent=2))

sample_input = X_test.iloc[[0]].copy()
sample_probability = float(best_model.predict_proba(sample_input)[0][1])
sample_prediction = bool(best_model.predict(sample_input)[0])

print("Пример single prediction:")
print({
    "prediction": sample_prediction,
    "prediction_label": "Покупка вероятна" if sample_prediction else "Покупка маловероятна",
    "purchase_probability": round(sample_probability, 4),
})
"""
            )
            break

    # Drop any leftover download section.
    cells[:] = [
        cell
        for cell in cells
        if "files.download" not in "".join(cell.get("source", []))
        and "# 16." not in "".join(cell.get("source", []))
    ]

    for cell in cells:
        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            cell["outputs"] = []

    for path in PATHS:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
