# evelyn/

Uyen's personal workspace for the Phase 2 handoff (post-MLHC-rejection methodology
plan, `Phase2_Methodology_Plan.pdf`). Scripts in here are working drafts for the four
advisor-assigned workstreams; outputs that the rest of the pipeline depends on are
written out to `data/` or `results/` per the plan, not kept only in here.

## Contents

- `workstream_a_scenario_pool/` — Workstream A: refine the 10,717-scenario base
  pool (`data/gen_prompts.csv`, `age_group == "base_prompt"`) into a curated
  200-scenario pool (`data/scenario_pool_v2.csv`) for hand annotation. Run
  `refine_scenario_pool.py`; see `selection_log.md` for the method, numbers,
  and known limitations.
- `workstream_b_age_relevance_taxonomy/` — Workstream B: the age_relevant /
  age_irrelevant / insufficient_context taxonomy. `taxonomy_guide_v1.md` is
  the guide (labels, ambiguous-case rule, worked examples). All 200 curated
  scenarios are labeled in `labeled_scenarios.csv`, which carries a
  `labeled_by` column tracking provenance: 30 scenarios are
  `human_consensus` (Evelyn and Chau independently agreed in a blind pilot,
  κ=0.535 on the 40-scenario sample), 10 are `human_evelyn_tiebreak`
  (pilot disagreements, Evelyn's label used as tie-break, noted as
  unresolved in `rationale`, `needs_clinical_review=yes`), and 160 are
  `ai_draft` (labeled directly by Claude per explicit instruction, not
  independently human-reviewed). **The 160 `ai_draft` rows are not validated
  ground truth** — treat them as a starting point for clinical/advisor
  review, not as equivalent to the pilot's human-labeled rows, since
  Workstream B exists specifically to avoid the single-AI-judge problem the
  original paper was rejected for. `build_pilot_sample.py` and
  `compute_agreement.py` remain as the tooling used to produce the pilot
  (regenerate a fresh pilot from `data/scenario_pool_v2.csv` if redoing this
  with full independent human review later).

Workstreams C (rubric tightening) and D (controlled computational pilot) will
get their own subfolders here as they're started.
