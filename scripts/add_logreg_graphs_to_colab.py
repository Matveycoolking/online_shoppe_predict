from __future__ import annotations

import json
from pathlib import Path


PATHS = [
    Path(r"C:\Users\matve\Downloads\online_shopper_intention_colab_improved_clean.ipynb"),
    Path(r"C:\Users\matve\Desktop\InternetBying\notebooks\online_shopper_intention_colab_improved_clean.ipynb"),
]


def source(text: str) -> list[str]:
    return [line + "\n" for line in text.strip("\n").split("\n")]


def markdown_cell(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source(text)}


def code_cell(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source(text),
    }


def main() -> None:
    nb = json.loads(PATHS[0].read_text(encoding="utf-8"))
    cells = nb["cells"]

    marker = "# 11.2. Графики для Logistic Regression"
    cells[:] = [cell for cell in cells if marker not in "".join(cell.get("source", []))]

    insert_after = None
    for index, cell in enumerate(cells):
        if cell.get("cell_type") == "code" and "Confusion matrix:" in "".join(cell.get("source", [])):
            insert_after = index + 1
            break

    if insert_after is None:
        raise ValueError("Could not find detailed metrics cell.")

    new_cells = [
        markdown_cell(
            """
# 11.2. Графики для Logistic Regression

Отдельно визуализирую baseline-модель Logistic Regression. Это помогает показать, как работает простая модель: где она ошибается, насколько хорошо разделяет классы и какие признаки сильнее всего влияют на прогноз.
"""
        ),
        code_cell(
            """
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_curve

logreg_pipeline = trained_models["Logistic Regression"]
logreg_pred = logreg_pipeline.predict(X_test)
logreg_proba = logreg_pipeline.predict_proba(X_test)[:, 1]

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 1. Confusion Matrix
logreg_cm = confusion_matrix(y_test, logreg_pred)
sns.heatmap(
    logreg_cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Нет покупки", "Покупка"],
    yticklabels=["Нет покупки", "Покупка"],
    ax=axes[0],
)
axes[0].set_title("Logistic Regression: Confusion Matrix")
axes[0].set_xlabel("Предсказанный класс")
axes[0].set_ylabel("Истинный класс")

# 2. ROC Curve
fpr, tpr, _ = roc_curve(y_test, logreg_proba)
logreg_auc = roc_auc_score(y_test, logreg_proba)
axes[1].plot(fpr, tpr, label=f"ROC-AUC = {logreg_auc:.3f}", color="#32C2D7", linewidth=2)
axes[1].plot([0, 1], [0, 1], linestyle="--", color="gray")
axes[1].set_title("Logistic Regression: ROC curve")
axes[1].set_xlabel("False Positive Rate")
axes[1].set_ylabel("True Positive Rate")
axes[1].legend()

# 3. Precision-Recall Curve
precision_curve, recall_curve, _ = precision_recall_curve(y_test, logreg_proba)
avg_precision = average_precision_score(y_test, logreg_proba)
axes[2].plot(recall_curve, precision_curve, label=f"AP = {avg_precision:.3f}", color="#89C400", linewidth=2)
axes[2].set_title("Logistic Regression: Precision-Recall curve")
axes[2].set_xlabel("Recall")
axes[2].set_ylabel("Precision")
axes[2].legend()

plt.tight_layout()
plt.show()
"""
        ),
        code_cell(
            """
logreg_preprocessor = logreg_pipeline.named_steps["preprocessor"]
logreg_model = logreg_pipeline.named_steps["model"]

try:
    logreg_feature_names = logreg_preprocessor.get_feature_names_out()
except Exception:
    logreg_feature_names = np.array(
        [f"feature_{i}" for i in range(logreg_preprocessor.transform(X_train.iloc[:1]).shape[1])]
    )

coef_df = pd.DataFrame(
    {
        "feature": logreg_feature_names,
        "coefficient": logreg_model.coef_[0],
    }
)
coef_df["abs_coefficient"] = coef_df["coefficient"].abs()
top_coef_df = coef_df.sort_values("abs_coefficient", ascending=False).head(15)

display(top_coef_df)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_coef_df,
    y="feature",
    x="coefficient",
    palette=["#89C400" if value > 0 else "#32C2D7" for value in top_coef_df["coefficient"]],
)
plt.axvline(0, color="black", linewidth=1)
plt.title("Logistic Regression: топ-15 коэффициентов")
plt.xlabel("Коэффициент")
plt.ylabel("Признак")
plt.tight_layout()
plt.show()

print(
    "Интерпретация: положительные коэффициенты повышают вероятность покупки, "
    "отрицательные — снижают. Значение важно сравнивать после preprocessing, "
    "так как числовые признаки масштабируются, а категориальные кодируются через OneHotEncoder."
)
"""
        ),
    ]

    cells[insert_after:insert_after] = new_cells

    for cell in cells:
        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            cell["outputs"] = []

    for path in PATHS:
        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
