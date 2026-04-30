"""Exploratory data analysis for the shopper intention dataset."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import FIGURES_DIR, REPORTS_DIR, TARGET_COLUMN
from src.data_loading import load_data

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


def basic_info(df: pd.DataFrame) -> dict[str, object]:
    """Return core dataset information."""
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }


def target_distribution(df: pd.DataFrame) -> pd.Series:
    """Return target counts."""
    return df[TARGET_COLUMN].value_counts(dropna=False)


def missing_values_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return missing value counts and shares by column."""
    missing_count = df.isna().sum()
    missing_share = (missing_count / len(df)).round(4)
    return pd.DataFrame(
        {
            "missing_count": missing_count,
            "missing_share": missing_share,
        }
    )


def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return descriptive statistics for numeric columns."""
    return df[NUMERIC_FEATURES].describe().T


def categorical_summary(df: pd.DataFrame) -> dict[str, pd.Series]:
    """Return value counts for categorical columns."""
    return {
        column: df[column].value_counts(dropna=False)
        for column in CATEGORICAL_FEATURES
    }


def _save_current_plot(filename: str) -> None:
    """Save current matplotlib figure and close it."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close()


def plot_target_distribution(df: pd.DataFrame) -> None:
    """Plot target class distribution."""
    plt.figure(figsize=(7, 5))
    ax = sns.countplot(data=df, x=TARGET_COLUMN, hue=TARGET_COLUMN, palette="Set2", legend=False)
    ax.set_title("Target Distribution")
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Number of sessions")
    _save_current_plot("target_distribution.png")


def plot_numeric_distributions(df: pd.DataFrame) -> None:
    """Plot distributions for key numeric features."""
    features_to_plot = {
        "PageValues": "pagevalues_distribution.png",
        "ExitRates": "exitrates_distribution.png",
        "BounceRates": "bouncerates_distribution.png",
    }

    for feature, filename in features_to_plot.items():
        plt.figure(figsize=(8, 5))
        ax = sns.histplot(data=df, x=feature, hue=TARGET_COLUMN, bins=40, kde=True)
        ax.set_title(f"{feature} Distribution by Revenue")
        ax.set_xlabel(feature)
        ax.set_ylabel("Number of sessions")
        _save_current_plot(filename)


def plot_correlation_matrix(df: pd.DataFrame) -> None:
    """Plot a correlation matrix for numeric features and the target."""
    corr_df = df[NUMERIC_FEATURES + [TARGET_COLUMN]].copy()
    corr_df[TARGET_COLUMN] = corr_df[TARGET_COLUMN].astype(int)
    correlation = corr_df.corr(numeric_only=True)

    plt.figure(figsize=(11, 8))
    ax = sns.heatmap(correlation, annot=True, fmt=".2f", cmap="vlag", center=0)
    ax.set_title("Correlation Matrix")
    _save_current_plot("correlation_matrix.png")


def plot_revenue_by_month(df: pd.DataFrame) -> None:
    """Plot purchase share by month."""
    month_order = ["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_revenue = (
        df.groupby("Month", observed=False)[TARGET_COLUMN]
        .mean()
        .reindex(month_order)
        .dropna()
        .reset_index()
    )

    plt.figure(figsize=(9, 5))
    ax = sns.barplot(data=monthly_revenue, x="Month", y=TARGET_COLUMN, color="#4c78a8")
    ax.set_title("Purchase Share by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Purchase share")
    _save_current_plot("revenue_by_month.png")


def plot_revenue_by_visitor_type(df: pd.DataFrame) -> None:
    """Plot purchase share by visitor type."""
    revenue_by_type = (
        df.groupby("VisitorType", observed=False)[TARGET_COLUMN]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    plt.figure(figsize=(8, 5))
    ax = sns.barplot(data=revenue_by_type, x="VisitorType", y=TARGET_COLUMN, color="#59a14f")
    ax.set_title("Purchase Share by Visitor Type")
    ax.set_xlabel("Visitor type")
    ax.set_ylabel("Purchase share")
    _save_current_plot("revenue_by_visitor_type.png")


def plot_revenue_by_weekend(df: pd.DataFrame) -> None:
    """Plot purchase share for weekday and weekend sessions."""
    revenue_by_weekend = (
        df.groupby("Weekend", observed=False)[TARGET_COLUMN]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(7, 5))
    ax = sns.barplot(data=revenue_by_weekend, x="Weekend", y=TARGET_COLUMN, color="#f28e2b")
    ax.set_title("Purchase Share by Weekend")
    ax.set_xlabel("Weekend")
    ax.set_ylabel("Purchase share")
    _save_current_plot("revenue_by_weekend.png")


def plot_numeric_boxplots(df: pd.DataFrame) -> None:
    """Save boxplots for numeric features to inspect outliers."""
    melted = df[NUMERIC_FEATURES].melt(var_name="feature", value_name="value")
    plt.figure(figsize=(13, 7))
    ax = sns.boxplot(data=melted, x="feature", y="value", color="#b07aa1")
    ax.set_title("Numeric Feature Boxplots")
    ax.set_xlabel("Feature")
    ax.set_ylabel("Value")
    plt.xticks(rotation=45, ha="right")
    _save_current_plot("numeric_boxplots.png")


def _markdown_table(df: pd.DataFrame) -> str:
    """Convert a DataFrame to a markdown table without optional dependencies."""
    table = df.reset_index()
    table = table.rename(columns={"index": "column"})
    table = table.astype(str)
    headers = list(table.columns)
    separator = ["---"] * len(headers)
    rows = [headers, separator] + table.values.tolist()
    return "\n".join("| " + " | ".join(row) + " |" for row in rows)


def create_eda_summary(df: pd.DataFrame) -> None:
    """Write a markdown EDA summary report."""
    info = basic_info(df)
    target_counts = target_distribution(df)
    purchase_share = float(df[TARGET_COLUMN].mean())
    missing_report = missing_values_report(df)
    numeric_stats = numeric_summary(df)

    lines = [
        "# EDA Summary",
        "",
        "## Размер датасета",
        "",
        f"- Строк: {info['shape'][0]}",
        f"- Столбцов: {info['shape'][1]}",
        "",
        "## Список колонок",
        "",
        "\n".join(f"- `{column}`" for column in info["columns"]),
        "",
        "## Типы данных",
        "",
        _markdown_table(pd.DataFrame.from_dict(info["dtypes"], orient="index", columns=["dtype"])),
        "",
        "## Пропуски",
        "",
        _markdown_table(missing_report),
        "",
        "## Распределение целевой переменной",
        "",
        _markdown_table(target_counts.rename("count").to_frame()),
        "",
        f"Доля покупок: {purchase_share:.2%}.",
        "",
        "Целевая переменная несбалансирована: покупок значительно меньше, чем сессий без покупки. "
        "Поэтому при оценке моделей необходимо использовать не только accuracy, но и precision, "
        "recall, F1-score и ROC-AUC.",
        "",
        "## Описательная статистика числовых признаков",
        "",
        _markdown_table(numeric_stats.round(4)),
        "",
        "## Краткие выводы",
        "",
        "- В датасете нет критических проблем со структурой: ожидаемые колонки присутствуют.",
        "- Покупки составляют меньшую часть наблюдений, поэтому задача чувствительна к дисбалансу классов.",
        "- Поведенческие признаки вроде `PageValues`, `ExitRates` и `BounceRates` важны для дальнейшего анализа.",
        "- Выбросы в поведенческих признаках могут отражать реальные сессии пользователей, поэтому они не удалялись автоматически.",
        "",
        "## Сохранённые графики",
        "",
        "- `reports/figures/target_distribution.png`",
        "- `reports/figures/correlation_matrix.png`",
        "- `reports/figures/revenue_by_month.png`",
        "- `reports/figures/revenue_by_visitor_type.png`",
        "- `reports/figures/revenue_by_weekend.png`",
        "- `reports/figures/pagevalues_distribution.png`",
        "- `reports/figures/exitrates_distribution.png`",
        "- `reports/figures/bouncerates_distribution.png`",
        "- `reports/figures/numeric_boxplots.png`",
        "",
    ]

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "eda_summary.md").write_text("\n".join(lines), encoding="utf-8")


def run_eda() -> None:
    """Run the full EDA pipeline and save reports and figures."""
    df = load_data()
    plot_target_distribution(df)
    plot_numeric_distributions(df)
    plot_correlation_matrix(df)
    plot_revenue_by_month(df)
    plot_revenue_by_visitor_type(df)
    plot_revenue_by_weekend(df)
    plot_numeric_boxplots(df)
    create_eda_summary(df)


if __name__ == "__main__":
    run_eda()
