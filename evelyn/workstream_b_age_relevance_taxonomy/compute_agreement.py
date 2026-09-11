"""
Workstream B -- Inter-rater agreement (Phase2_Methodology_Plan.pdf, Section
2B, step 6).

Reads the two independently-completed pilot annotation sheets
(annotation_sheet_reviewer_a.csv, annotation_sheet_reviewer_b.csv, produced
blank by build_pilot_sample.py and then filled in by two people), validates
the insufficient_context rule, and computes percent agreement + Cohen's kappa
on proposed_label -- before any disagreement is resolved, per the plan
("agreement measures consistency; it does not establish clinical
correctness").

Run this only after both sheets are filled in.

Usage:
    python evelyn/workstream_b_age_relevance_taxonomy/compute_agreement.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

OUTPUT_DIR = Path(__file__).resolve().parent
REVIEWER_A_PATH = OUTPUT_DIR / "annotation_sheet_reviewer_a.csv"
REVIEWER_B_PATH = OUTPUT_DIR / "annotation_sheet_reviewer_b.csv"
REPORT_PATH = OUTPUT_DIR / "agreement_report.md"

VALID_LABELS = {"age_relevant", "age_irrelevant", "insufficient_context"}


def _load_completed_sheet(path: Path, reviewer_name: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run build_pilot_sample.py first, then have "
            f"{reviewer_name} fill it in before running this script."
        )
    df = pd.read_csv(path)
    blank_labels = df["proposed_label"].isna() | (df["proposed_label"].astype(str).str.strip() == "")
    if blank_labels.any():
        raise ValueError(
            f"{path} has {blank_labels.sum()} row(s) with an empty proposed_label "
            f"-- {reviewer_name}'s sheet isn't fully filled in yet."
        )
    return df


def _validate_insufficient_context_rule(df: pd.DataFrame, reviewer_name: str) -> list[str]:
    """The guide requires missing_context_factors to be non-empty whenever
    proposed_label OR secondary_label is insufficient_context -- naming the
    label alone ("I don't know") isn't a valid entry."""
    violations = []
    is_insufficient = (df["proposed_label"] == "insufficient_context") | (
        df.get("secondary_label", pd.Series(dtype=str)) == "insufficient_context"
    )
    missing_factors = df["missing_context_factors"].isna() | (
        df["missing_context_factors"].astype(str).str.strip() == ""
    )
    bad_rows = df[is_insufficient & missing_factors]
    for _, row in bad_rows.iterrows():
        violations.append(
            f"{reviewer_name}, scenario_id {row['scenario_id']}: labeled "
            f"insufficient_context (primary or secondary) but "
            f"missing_context_factors is empty."
        )
    return violations


def _unrecognized_labels(df: pd.DataFrame, reviewer_name: str) -> list[str]:
    bad = df.loc[~df["proposed_label"].isin(VALID_LABELS), ["scenario_id", "proposed_label"]]
    return [
        f"{reviewer_name}, scenario_id {row.scenario_id}: unrecognized label "
        f"{row.proposed_label!r} (expected one of {sorted(VALID_LABELS)})"
        for row in bad.itertuples()
    ]


def _cohens_kappa(labels_a: pd.Series, labels_b: pd.Series) -> float:
    n = len(labels_a)
    po = (labels_a.to_numpy() == labels_b.to_numpy()).mean()

    all_labels = sorted(set(labels_a) | set(labels_b))
    pe = sum(
        (labels_a == label).mean() * (labels_b == label).mean() for label in all_labels
    )
    if pe == 1.0:
        return 1.0 if po == 1.0 else 0.0
    return (po - pe) / (1 - pe)


def _confusion_matrix(labels_a: pd.Series, labels_b: pd.Series) -> pd.DataFrame:
    return pd.crosstab(labels_a, labels_b, rownames=["reviewer_a"], colnames=["reviewer_b"])


def _markdown_table(df: pd.DataFrame) -> str:
    # Avoids depending on the optional `tabulate` package that
    # DataFrame.to_markdown() requires but isn't in requirements.txt.
    header = ["reviewer_a \\ reviewer_b"] + [str(c) for c in df.columns]
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for index, row in df.iterrows():
        lines.append("| " + " | ".join([str(index)] + [str(v) for v in row]) + " |")
    return "\n".join(lines)


def compute_agreement() -> None:
    sheet_a = _load_completed_sheet(REVIEWER_A_PATH, "reviewer_a")
    sheet_b = _load_completed_sheet(REVIEWER_B_PATH, "reviewer_b")

    if set(sheet_a["scenario_id"]) != set(sheet_b["scenario_id"]):
        raise ValueError(
            "reviewer_a and reviewer_b sheets don't cover the same scenario_id "
            "set -- did one get edited (rows added/removed) after "
            "build_pilot_sample.py generated them?"
        )

    violations = (
        _validate_insufficient_context_rule(sheet_a, "reviewer_a")
        + _validate_insufficient_context_rule(sheet_b, "reviewer_b")
        + _unrecognized_labels(sheet_a, "reviewer_a")
        + _unrecognized_labels(sheet_b, "reviewer_b")
    )

    merged = sheet_a.merge(
        sheet_b, on=["scenario_id", "question", "category"], suffixes=("_a", "_b")
    ).sort_values("scenario_id")

    agree_mask = merged["proposed_label_a"] == merged["proposed_label_b"]
    percent_agreement = agree_mask.mean()
    kappa = _cohens_kappa(merged["proposed_label_a"], merged["proposed_label_b"])
    confusion = _confusion_matrix(merged["proposed_label_a"], merged["proposed_label_b"])

    _write_report(merged, agree_mask, percent_agreement, kappa, confusion, violations)

    print(f"n = {len(merged)} scenarios")
    print(f"Percent agreement: {percent_agreement:.1%}")
    print(f"Cohen's kappa: {kappa:.3f}")
    print(f"Validation violations: {len(violations)}")
    print(f"Wrote {REPORT_PATH}")


def _write_report(
    merged: pd.DataFrame,
    agree_mask: pd.Series,
    percent_agreement: float,
    kappa: float,
    confusion: pd.DataFrame,
    violations: list[str],
) -> None:
    disagreements = merged[~agree_mask]

    lines = [
        "# Workstream B -- Pilot Agreement Report",
        "",
        f"n = {len(merged)} scenarios, both reviewers.",
        "",
        "**Agreement measures consistency, not clinical correctness** -- two "
        "reviewers agreeing doesn't mean the label is right, only that the "
        "guide is being applied the same way. Resolve disagreements only "
        "after recording these numbers, and keep the original two sheets "
        "unchanged when you do.",
        "",
        "## Headline numbers",
        "",
        f"- Percent agreement: **{percent_agreement:.1%}**",
        f"- Cohen's kappa: **{kappa:.3f}**",
        "",
        "## Validation issues",
        "",
    ]
    if violations:
        lines.append(
            f"**{len(violations)} row(s) violate the insufficient_context rule "
            "or use an unrecognized label** -- fix these in the source sheet "
            "and rerun before trusting the agreement numbers above:"
        )
        lines += [f"- {v}" for v in violations]
    else:
        lines.append("None found.")

    lines += [
        "",
        "## Confusion matrix (reviewer_a rows x reviewer_b columns)",
        "",
        _markdown_table(confusion),
        "",
        f"## Disagreements ({len(disagreements)} of {len(merged)})",
        "",
    ]
    if disagreements.empty:
        lines.append("None -- full agreement on this pilot sample.")
    else:
        for _, row in disagreements.iterrows():
            lines += [
                f"### scenario_id {row['scenario_id']} ({row['category']})",
                "",
                f"> {row['question']}",
                "",
                f"- reviewer_a: `{row['proposed_label_a']}` -- {row['rationale_a']}",
                f"- reviewer_b: `{row['proposed_label_b']}` -- {row['rationale_b']}",
                "",
            ]

    REPORT_PATH.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    compute_agreement()
