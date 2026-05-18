from __future__ import annotations

import json
from pathlib import Path


DOWNLOADS = Path(r"C:\Users\matve\Downloads")
PROJECT = Path(r"C:\Users\matve\Desktop\InternetBying")
INPUT = DOWNLOADS / "online_shopper_intention_colab_improved.ipynb"
OUTPUT_DOWNLOADS = DOWNLOADS / "online_shopper_intention_colab_improved_clean.ipynb"
OUTPUT_PROJECT = PROJECT / "notebooks" / "online_shopper_intention_colab_improved_clean.ipynb"


def source(text: str) -> list[str]:
    return [line + "\n" for line in text.strip("\n").split("\n")]


def find_cell(cells: list[dict], marker: str, cell_type: str | None = None) -> int:
    for index, cell in enumerate(cells):
        if cell_type is not None and cell.get("cell_type") != cell_type:
            continue
        if marker in "".join(cell.get("source", [])):
            return index
    raise ValueError(f"Cell with marker not found: {marker}")


def main() -> None:
    nb = json.loads(INPUT.read_text(encoding="utf-8"))
    cells = nb["cells"]

    cells[find_cell(cells, "# 8.1.", "markdown")]["source"] = source(
        """
# 8.1. Feature engineering

Чтобы усилить проект, добавляю несколько новых признаков, которые логично описывают поведение пользователя в сессии.

Новые признаки:

- `TotalPages` — общее число просмотренных страниц;
- `TotalDuration` — общая длительность сессии по основным группам страниц;
- `ProductPagesShare` — доля товарных страниц среди всех просмотренных страниц;
- `AvgProductDuration` — среднее время на одной товарной странице;
- `HasPageValue` — есть ли у сессии ненулевое значение `PageValues`.

Эти признаки помогают модели учитывать не только отдельные исходные колонки, но и агрегированную вовлечённость пользователя.
"""
    )

    cells[find_cell(cells, 'df_model = df.copy()', "code")]["source"] = source(
        """
df_model = df.copy()

df_model["TotalPages"] = (
    df_model["Administrative"]
    + df_model["Informational"]
    + df_model["ProductRelated"]
)

df_model["TotalDuration"] = (
    df_model["Administrative_Duration"]
    + df_model["Informational_Duration"]
    + df_model["ProductRelated_Duration"]
)

df_model["ProductPagesShare"] = np.where(
    df_model["TotalPages"] > 0,
    df_model["ProductRelated"] / df_model["TotalPages"],
    0.0,
)

df_model["AvgProductDuration"] = np.where(
    df_model["ProductRelated"] > 0,
    df_model["ProductRelated_Duration"] / df_model["ProductRelated"],
    0.0,
)

df_model["HasPageValue"] = (df_model["PageValues"] > 0).astype(int)

ENGINEERED_NUMERIC_FEATURES = [
    "TotalPages",
    "TotalDuration",
    "ProductPagesShare",
    "AvgProductDuration",
    "HasPageValue",
]

NUMERIC_FEATURES = NUMERIC_FEATURES + ENGINEERED_NUMERIC_FEATURES

print("Добавлены новые признаки:")
display(df_model[ENGINEERED_NUMERIC_FEATURES].head())
display(
    df_model[ENGINEERED_NUMERIC_FEATURES + [TARGET_COLUMN]]
    .corr(numeric_only=True)[[TARGET_COLUMN]]
    .sort_values(TARGET_COLUMN, ascending=False)
)
"""
    )

    cells[find_cell(cells, "# 10.1.", "markdown")]["source"] = source(
        """
# 10.1. Подбор гиперпараметров

Для усиления проекта добавляю `RandomizedSearchCV` для Random Forest. Это показывает, что модель не просто взята с фиксированными параметрами, а основные гиперпараметры были подобраны по кросс-валидации.

Чтобы ноутбук запускался быстрее, поиск ограничен небольшим числом комбинаций.
"""
    )

    cells[find_cell(cells, "rf_search = RandomizedSearchCV", "code")]["source"] = source(
        """
cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=RANDOM_STATE)

rf_pipeline = Pipeline(
    steps=[
        ("preprocessor", build_preprocessor()),
        ("model", RandomForestClassifier(class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1)),
    ]
)

rf_param_distributions = {
    "model__n_estimators": [200, 300, 500],
    "model__max_depth": [None, 6, 10, 14],
    "model__min_samples_split": [2, 5, 10],
    "model__min_samples_leaf": [1, 2, 4],
    "model__max_features": ["sqrt", "log2", None],
}

rf_search = RandomizedSearchCV(
    estimator=rf_pipeline,
    param_distributions=rf_param_distributions,
    n_iter=8,
    scoring="f1",
    cv=cv,
    random_state=RANDOM_STATE,
    n_jobs=-1,
    verbose=1,
)

rf_search.fit(X_train, y_train)
print("Лучшие параметры Random Forest:")
print(rf_search.best_params_)
print(f"Лучший CV F1: {rf_search.best_score_:.4f}")

tuned_rf = rf_search.best_estimator_
tuned_rf_metrics = evaluate_model(tuned_rf, X_test, y_test)

trained_models["Random Forest Tuned"] = tuned_rf
metrics_by_model["Random Forest Tuned"] = tuned_rf_metrics
comparison = pd.concat(
    [comparison, pd.DataFrame([metrics_row("Random Forest Tuned", tuned_rf_metrics)])],
    ignore_index=True,
).sort_values(by=["f1", "roc_auc"], ascending=False)

display(comparison)
"""
    )

    cells[find_cell(cells, "# 11.1.", "markdown")]["source"] = source(
        """
# 11.1. Кросс-валидация лучшей модели

Дополнительно проверяю лучшую модель через `StratifiedKFold`. Это снижает зависимость оценки от одного разбиения train/test и усиливает раздел про корректность валидации.
"""
    )

    cells[find_cell(cells, "cv_scores = cross_validate", "code")]["source"] = source(
        """
current_best_model_name = str(comparison.iloc[0]["model"])
current_best_model = trained_models[current_best_model_name]

cv_scores = cross_validate(
    current_best_model,
    X_train,
    y_train,
    cv=cv,
    scoring={
        "accuracy": "accuracy",
        "precision": "precision",
        "recall": "recall",
        "f1": "f1",
        "roc_auc": "roc_auc",
    },
    n_jobs=-1,
)

cv_summary = pd.DataFrame(
    {
        metric.replace("test_", ""): [scores.mean(), scores.std()]
        for metric, scores in cv_scores.items()
        if metric.startswith("test_")
    },
    index=["mean", "std"],
).T

print(f"Кросс-валидация для модели: {current_best_model_name}")
display(cv_summary)
"""
    )

    cells[find_cell(cells, "best_model_name = str(comparison.iloc[0]", "code")]["source"] = source(
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

    cells[find_cell(cells, "# 13.", "markdown")]["source"] = source(
        """
# 13. Train/test comparison и анализ переобучения

Сравниваю качество лучшей модели на train и test. Если train-метрики намного выше test-метрик, это признак возможного переобучения.
"""
    )

    cells[find_cell(cells, "train_metrics = evaluate_model", "code")]["source"] = source(
        """
train_metrics = evaluate_model(best_model, X_train, y_train)
test_metrics = evaluate_model(best_model, X_test, y_test)

train_test_comparison = pd.DataFrame(
    [
        {"sample": "train", **{k: train_metrics[k] for k in ["accuracy", "precision", "recall", "f1", "roc_auc"]}},
        {"sample": "test", **{k: test_metrics[k] for k in ["accuracy", "precision", "recall", "f1", "roc_auc"]}},
    ]
)

display(train_test_comparison)

f1_gap = train_metrics["f1"] - test_metrics["f1"]
print(f"Разница train F1 - test F1: {f1_gap:.4f}")
if f1_gap > 0.10:
    print("Есть признаки переобучения: качество на train заметно выше, чем на test.")
else:
    print("Сильного переобучения по F1 не видно: train и test достаточно близки.")
"""
    )

    cells[find_cell(cells, "# 14.", "markdown")]["source"] = source(
        """
# 14. Интерпретация: важность признаков

Для лучшей модели вывожу топ важных признаков. Это помогает объяснить, какие факторы сильнее всего влияют на прогноз покупки.
"""
    )

    cells[find_cell(cells, "def get_transformed_feature_names", "code")]["source"] = source(
        """
def get_transformed_feature_names(pipeline: Pipeline) -> np.ndarray:
    preprocessor = pipeline.named_steps["preprocessor"]
    try:
        return preprocessor.get_feature_names_out()
    except Exception:
        return np.array([f"feature_{i}" for i in range(preprocessor.transform(X_train.iloc[:1]).shape[1])])


def get_model_importances(pipeline: Pipeline) -> np.ndarray:
    model = pipeline.named_steps["model"]
    if hasattr(model, "get_feature_importance"):
        return np.asarray(model.get_feature_importance())
    if hasattr(model, "feature_importances_"):
        return np.asarray(model.feature_importances_)
    if hasattr(model, "coef_"):
        return np.abs(model.coef_[0])
    raise AttributeError("Для этой модели нет встроенной важности признаков.")


try:
    feature_names = get_transformed_feature_names(best_model)
    importances = get_model_importances(best_model)
    importance_df = pd.DataFrame({"feature": feature_names, "importance": importances})
    importance_df = importance_df.sort_values("importance", ascending=False).head(15)

    display(importance_df)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=importance_df, y="feature", x="importance", color="#32C2D7")
    plt.title(f"Top-15 feature importance: {best_model_name}")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.tight_layout()
    plt.show()
except Exception as error:
    print(f"Не удалось получить важность признаков: {error}")
"""
    )

    cells[find_cell(cells, "# 15.", "markdown")]["source"] = source(
        """
# 15. Error analysis: разбор ошибок

Смотрю примеры корректных и ошибочных предсказаний. Это помогает понять, где модель ошибается: например, когда вероятность покупки высокая, но пользователь фактически не купил, или наоборот.
"""
    )

    cells[find_cell(cells, "y_test_pred = best_model.predict", "code")]["source"] = source(
        """
y_test_pred = best_model.predict(X_test)
y_test_proba = best_model.predict_proba(X_test)[:, 1]

error_df = X_test.copy()
error_df["y_true"] = y_test.values
error_df["y_pred"] = y_test_pred
error_df["purchase_probability"] = y_test_proba

conditions = [
    (error_df["y_true"] == 1) & (error_df["y_pred"] == 1),
    (error_df["y_true"] == 0) & (error_df["y_pred"] == 0),
    (error_df["y_true"] == 0) & (error_df["y_pred"] == 1),
    (error_df["y_true"] == 1) & (error_df["y_pred"] == 0),
]
choices = ["True Positive", "True Negative", "False Positive", "False Negative"]
error_df["case_type"] = np.select(conditions, choices, default="Other")

case_counts = error_df["case_type"].value_counts()
display(case_counts.to_frame("count"))

for case_type in choices:
    print(f"\\n=== {case_type} ===")
    display(
        error_df[error_df["case_type"] == case_type]
        .sort_values("purchase_probability", ascending=False)
        .head(3)[[
            "case_type",
            "y_true",
            "y_pred",
            "purchase_probability",
            "PageValues",
            "ExitRates",
            "BounceRates",
            "ProductRelated",
            "ProductRelated_Duration",
            "VisitorType",
            "Month",
        ]]
    )

print(
    "Вывод: false negative важны для бизнеса, потому что это реальные покупки, "
    "которые модель не нашла. False positive менее критичны, но могут приводить "
    "к лишним маркетинговым действиям."
)
"""
    )

    # Remove the final download section entirely.
    cells[:] = [
        cell
        for cell in cells
        if "# 16." not in "".join(cell.get("source", []))
        and "files.download" not in "".join(cell.get("source", []))
    ]

    for cell in cells:
        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            cell["outputs"] = []

    OUTPUT_PROJECT.parent.mkdir(parents=True, exist_ok=True)
    for path in (OUTPUT_DOWNLOADS, OUTPUT_PROJECT):
        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
