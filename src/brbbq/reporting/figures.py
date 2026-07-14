"""Paper-oriented figures for bilingual and Brazil-specific analyses."""

from pathlib import Path
from typing import Dict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


COLORS = {"pt": "#176B87", "en": "#D97706", "neutral": "#52616B", "accent": "#A23B72"}


def _save(fig, path: Path) -> None:
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def _grouped(frame, index, columns, values):
    return frame.pivot(index=index, columns=columns, values=values)


def generate_figures(
    predictions: pd.DataFrame, tables: Dict[str, pd.DataFrame], figure_dir: Path
) -> None:
    figure_dir.mkdir(parents=True, exist_ok=True)
    by_lang_context = tables["by_language_context"]
    pivot = _grouped(by_lang_context, "context_type", "language", "accuracy")
    ax = pivot.plot(
        kind="bar",
        color=[COLORS.get(c, COLORS["neutral"]) for c in pivot.columns],
        figsize=(6.5, 4),
    )
    ax.set(
        title="Accuracy by language and context", xlabel="Context", ylabel="Accuracy", ylim=(0, 1)
    )
    ax.legend(title="Language")
    _save(ax.figure, figure_dir / "01_accuracy_language_context.png")

    by_cat_lang = tables["by_category_language"]
    pivot = _grouped(by_cat_lang, "category_id", "language", "s_DIS")
    ax = pivot.plot(
        kind="bar",
        color=[COLORS.get(c, COLORS["neutral"]) for c in pivot.columns],
        figsize=(10, 4.8),
    )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set(
        title="Disambiguated bias score by category and language",
        xlabel="Category",
        ylabel="s_DIS",
        ylim=(-1, 1),
    )
    ax.legend(title="Language")
    _save(ax.figure, figure_dir / "02_bias_category_language.png")

    paired_cat = tables["paired_by_category"].set_index("category_id")
    ax = paired_cat[["accuracy_diff_pt_minus_en", "unknown_rate_diff_pt_minus_en"]].plot(
        kind="bar", color=[COLORS["pt"], COLORS["accent"]], figsize=(10, 4.8)
    )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set(
        title="Portuguese minus English differences by category",
        xlabel="Category",
        ylabel="Difference",
    )
    _save(ax.figure, figure_dir / "03_pt_en_difference_category.png")

    letter = tables["by_language"].set_index("language")[["rate_A", "rate_B", "rate_C"]]
    ax = letter.plot(kind="bar", color=["#176B87", "#D97706", "#A23B72"], figsize=(6.5, 4))
    ax.set(
        title="A/B/C response distribution by language",
        xlabel="Language",
        ylabel="Rate",
        ylim=(0, 1),
    )
    _save(ax.figure, figure_dir / "04_letter_distribution_language.png")

    pos = tables["by_unknown_position_language"]
    pivot = _grouped(pos, "unknown_position", "language", "unknown_rate")
    ax = pivot.plot(
        kind="bar",
        color=[COLORS.get(c, COLORS["neutral"]) for c in pivot.columns],
        figsize=(6.5, 4),
    )
    ax.set(
        title="Unknown rate by option position and language",
        xlabel="Unknown position",
        ylabel="Unknown rate",
        ylim=(0, 1),
    )
    _save(ax.figure, figure_dir / "05_unknown_rate_position_language.png")

    positional = tables["by_language"].set_index("language")[["position_consistency", "flip_rate"]]
    ax = positional.plot(kind="bar", color=[COLORS["neutral"], COLORS["accent"]], figsize=(6.5, 4))
    ax.set(
        title="Position consistency and flip rate", xlabel="Language", ylabel="Rate", ylim=(0, 1)
    )
    _save(ax.figure, figure_dir / "06_position_consistency_flip_rate.png")

    transition = tables["transition"].set_index("selected_content_pt")
    matrix = transition[["group1", "group2", "unknown"]].to_numpy(dtype=float)
    row_sums = matrix.sum(axis=1, keepdims=True)
    normalized = np.divide(matrix, row_sums, out=np.zeros_like(matrix), where=row_sums != 0)
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    image = ax.imshow(normalized, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(3))
    ax.set_xticklabels(["group1", "group2", "unknown"])
    ax.set_yticks(range(3))
    ax.set_yticklabels(["group1", "group2", "unknown"])
    ax.set(
        xlabel="Selected content in English",
        ylabel="Selected content in Portuguese",
        title="PT-to-EN semantic transition matrix",
    )
    for i in range(3):
        for j in range(3):
            ax.text(j, i, "{:.2f}".format(normalized[i, j]), ha="center", va="center")
    fig.colorbar(image, ax=ax, label="Row proportion")
    _save(fig, figure_dir / "07_pt_en_transition_heatmap.png")

    for number, category, title in (
        (8, "regionality", "Regionality: PT vs EN"),
        (9, "religion", "Religion: PT vs EN"),
    ):
        subset = by_cat_lang[by_cat_lang["category_id"] == category].set_index("language")[
            ["accuracy", "unknown_rate", "s_DIS", "s_AMB"]
        ]
        if subset.empty:
            subset = pd.DataFrame(
                {
                    "accuracy": [np.nan],
                    "unknown_rate": [np.nan],
                    "s_DIS": [np.nan],
                    "s_AMB": [np.nan],
                },
                index=["unavailable"],
            )
        ax = subset.plot(
            kind="bar", color=["#176B87", "#D97706", "#52616B", "#A23B72"], figsize=(7, 4.2)
        )
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set(title=title, xlabel="Language", ylabel="Metric", ylim=(-1, 1))
        _save(ax.figure, figure_dir / "{:02d}_{}_specific.png".format(number, category))

    aggregation = tables["by_aggregation_language"]
    pivot = _grouped(aggregation, "aggregation", "language", "accuracy")
    ax = pivot.plot(
        kind="bar",
        color=[COLORS.get(c, COLORS["neutral"]) for c in pivot.columns],
        figsize=(7, 4.2),
    )
    ax.set(
        title="Core, exploratory, and Brazil-specific category results",
        xlabel="Aggregation",
        ylabel="Accuracy",
        ylim=(0, 1),
    )
    _save(ax.figure, figure_dir / "10_general_brazilian_categories.png")
