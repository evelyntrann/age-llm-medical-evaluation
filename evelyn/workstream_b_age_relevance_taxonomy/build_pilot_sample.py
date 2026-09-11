"""
Workstream B -- Pilot sample + annotation sheets (Phase2_Methodology_Plan.pdf,
Section 2B, steps 1 and 5).

Draws a stratified pilot sample (default 40, plan range 30-50) from the curated
200-scenario pool (data/scenario_pool_v2.csv) and writes two IDENTICAL, BLANK
annotation sheets -- one per reviewer -- so two people can label the same
scenarios independently without seeing each other's answers. Also writes a
blank sheet for the remaining (non-pilot) scenarios, ready for the single-pass
"apply the revised guide to the remaining pool" step once the pilot agreement
check is done (step 7 of the plan) -- that step still requires a human to
actually fill it in; this script only prepares the template.

This script does NOT propose any labels. Labeling is the human (or
advisor/clinical-collaborator) task the pilot is designed to validate --
auto-filling it here would recreate exactly the single-annotator problem the
MLHC reviewers flagged.

Usage:
    python evelyn/workstream_b_age_relevance_taxonomy/build_pilot_sample.py
    python evelyn/workstream_b_age_relevance_taxonomy/build_pilot_sample.py --pilot-size 30
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
CURATED_POOL_CSV_PATH = REPO_ROOT / "data" / "scenario_pool_v2.csv"
OUTPUT_DIR = Path(__file__).resolve().parent

DEFAULT_PILOT_SIZE = 40
RANDOM_SEED = 42

SHEET_COLUMNS = [
    "scenario_id", "question", "category", "proposed_label", "secondary_label",
    "rationale", "missing_context_factors", "needs_clinical_review",
]


def _stratified_pilot_ids(pool: pd.DataFrame, pilot_size: int, seed: int) -> set[int]:
    """Same proportional-quota approach as Workstream A's sampler, applied to
    the already-curated 200-row pool instead of the full 10,717-row one."""
    rng = np.random.default_rng(seed)
    category_counts = pool["category"].value_counts()
    total = len(pool)
    selected: set[int] = set()

    quotas = {
        category: max(1, round(pilot_size * count / total))
        for category, count in category_counts.items()
    }

    for category, quota in quotas.items():
        candidates = pool.loc[pool["category"] == category, "id"].to_numpy()
        take = min(quota, len(candidates), pilot_size - len(selected))
        if take <= 0:
            continue
        chosen = rng.choice(candidates, size=take, replace=False)
        selected.update(chosen.tolist())

    if len(selected) < pilot_size:
        remaining = pool.loc[~pool["id"].isin(selected), "id"].to_numpy()
        shortfall = pilot_size - len(selected)
        if len(remaining) > 0:
            top_up = rng.choice(remaining, size=min(shortfall, len(remaining)), replace=False)
            selected.update(top_up.tolist())

    return selected


def _blank_sheet(scenarios: pd.DataFrame) -> pd.DataFrame:
    sheet = scenarios.rename(columns={"id": "scenario_id"})[["scenario_id", "question", "category"]].copy()
    for col in ["proposed_label", "secondary_label", "rationale", "missing_context_factors", "needs_clinical_review"]:
        sheet[col] = ""
    return sheet[SHEET_COLUMNS]


def build_pilot_sample(pilot_size: int = DEFAULT_PILOT_SIZE, seed: int = RANDOM_SEED) -> None:
    pool = pd.read_csv(CURATED_POOL_CSV_PATH)
    pilot_ids = _stratified_pilot_ids(pool, pilot_size, seed)

    pilot = pool[pool["id"].isin(pilot_ids)].sort_values("id")
    remaining = pool[~pool["id"].isin(pilot_ids)].sort_values("id")

    reviewer_a_sheet = _blank_sheet(pilot)
    reviewer_b_sheet = _blank_sheet(pilot)
    remaining_sheet = _blank_sheet(remaining)

    reviewer_a_path = OUTPUT_DIR / "annotation_sheet_reviewer_a.csv"
    reviewer_b_path = OUTPUT_DIR / "annotation_sheet_reviewer_b.csv"
    remaining_path = OUTPUT_DIR / "remaining_pool_annotation_sheet.csv"

    reviewer_a_sheet.to_csv(reviewer_a_path, index=False)
    reviewer_b_sheet.to_csv(reviewer_b_path, index=False)
    remaining_sheet.to_csv(remaining_path, index=False)

    _write_manifest(pool, pilot, remaining, pilot_size, seed)

    print(f"Wrote {reviewer_a_path} ({len(pilot)} rows, blank)")
    print(f"Wrote {reviewer_b_path} ({len(pilot)} rows, blank -- identical scenarios)")
    print(f"Wrote {remaining_path} ({len(remaining)} rows, blank -- for step 7, after the pilot)")
    print(f"Wrote {OUTPUT_DIR / 'pilot_sample_manifest.md'}")


def _write_manifest(
    pool: pd.DataFrame, pilot: pd.DataFrame, remaining: pd.DataFrame, pilot_size: int, seed: int
) -> None:
    category_table = (
        pool.groupby("category")
        .agg(total=("id", "count"))
        .join(pilot.groupby("category").agg(pilot=("id", "count")))
        .fillna(0)
        .astype({"pilot": int})
        .sort_values("total", ascending=False)
    )

    lines = [
        "# Workstream B -- Pilot Sample Manifest",
        "",
        f"Source: `data/scenario_pool_v2.csv` ({len(pool)} curated scenarios).",
        f"Pilot target size: {pilot_size}; actual: {len(pilot)}. Random seed: {seed}.",
        f"Remaining pool (for step 7, after pilot agreement is checked): {len(remaining)} scenarios.",
        "",
        "## Category breakdown",
        "",
        "| Category | Total in curated pool | In pilot sample |",
        "|---|---|---|",
    ]
    for category, row in category_table.iterrows():
        lines.append(f"| {category} | {row['total']} | {row['pilot']} |")

    lines += [
        "",
        "## Pilot scenario IDs",
        "",
        ", ".join(str(i) for i in sorted(pilot["id"].tolist())),
        "",
        "## Notes",
        "",
        "- `annotation_sheet_reviewer_a.csv` and `annotation_sheet_reviewer_b.csv` "
        "contain the identical set of scenarios, blank label fields. Two people "
        "fill these in independently, without seeing each other's answers, per "
        "`taxonomy_guide_v1.md` Section 7.",
        "- `remaining_pool_annotation_sheet.csv` is a template for step 7 (apply "
        "the revised guide to the rest of the pool) -- not meant to be filled in "
        "until after the pilot agreement check and any guide revision.",
        "- Sampling is proportional-quota by Workstream A category, same method "
        "as `refine_scenario_pool.py`, so the pilot doesn't over-represent "
        "`other_general` (the largest category) at the expense of everything "
        "else.",
    ]

    (OUTPUT_DIR / "pilot_sample_manifest.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot-size", type=int, default=DEFAULT_PILOT_SIZE)
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    args = parser.parse_args()
    build_pilot_sample(pilot_size=args.pilot_size, seed=args.seed)
