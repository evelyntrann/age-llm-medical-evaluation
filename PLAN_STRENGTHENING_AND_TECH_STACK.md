# Staff-Level Review: Strengthening the Study and Choosing the Technical Stack

**Date:** September 2, 2026

## Assessment

The revised plan is materially stronger than the inherited study because it repairs the causal comparison, defines fairness clinically, introduces a human gold standard, uses paired inference, validates automated judges, and includes an actual mitigation experiment. Its main remaining risk is trying to obtain scale before the clinical construct and gold-standard rubric are stable.

The central scientific contribution should be a **two-sided age-relevance evaluation**:

- **Over-conditioning:** the model changes clinical advice when age should not matter.
- **Under-conditioning:** the model fails to change advice when age should matter.
- **Harmful adaptation:** the model changes advice in an unsafe or unsupported direction.
- **Appropriate adaptation:** the model makes the clinically expected change.

This is stronger than treating every difference from an age-unspecified answer as evidence of bias.

## Comparison with the inherited study

| Dimension | Inherited study | Revised plan | Why the revision is stronger |
|---|---|---|---|
| Intervention | An LLM rewrites age variants and also changes symptoms/context | Deterministic insertion changes age only | Supports a causal interpretation of age conditioning |
| Fairness definition | Any safety/tone difference can be interpreted as age bias | Clinicians define when adaptation is expected | Separates equitable personalization from stereotyping |
| Evaluation | One context-free LLM judge | Two clinicians plus calibrated, context-aware automated judges | Establishes a defensible gold standard and tests evaluator bias |
| Outcomes | Ad hoc aggregate safety, severity, and tone indices | Over-conditioning, under-conditioning, harmful adaptation, and absolute answer quality | Produces clinically interpretable endpoints |
| Analysis | Row-order grouping and mostly averages | Stable IDs, within-scenario pairs, confidence intervals, and clustered models | Preserves pairing and quantifies uncertainty |
| Models | One small open model and one closed model | Four complementary frozen model families | Improves relevance and comparative validity |
| Mitigation | Claimed but not evaluated | Prespecified intervention with benefit-preservation criterion | Tests a concrete response to the diagnosed failure |
| Reproducibility | Notebook state, manual copying, incomplete artifacts | Versioned Python pipeline, schemas, manifests, tests, and immutable outputs | Makes every result traceable and regenerable |

## Critical additions

1. **Clinician-defined expected behavior before model generation.** For each gold-core scenario, record whether age should matter, which response dimensions may change, and the expected direction. This prevents the gold label from being invented after seeing model answers.
2. **Two-level human scoring.** Clinicians should first score each answer independently for clinical quality and then compare the pair for appropriateness. Otherwise a pair can appear invariant even when both answers are unsafe.
3. **A tiered benchmark.** Build a clinician-validated gold core first and an extended automatically screened set only if time permits. Four hundred excellent scenarios are more valuable than one thousand noisy ones.
4. **A pilot-based power and workload calculation.** Freeze the final sample size, minimum detectable effect, primary endpoints, exclusions, and evaluator thresholds after the pilot but before the full run.
5. **A held-out test split.** Develop the rubric and mitigation on the pilot/development cases; report final performance once on an untouched, stratified test set.

## High-impact stretch goal

If clinician time permits, add a small **clinical-mediator factorial challenge set** of roughly 100 scenarios. For each scenario, construct four conditions: neither age nor mediator, age only, mediator only, and age plus mediator. A mediator is an explicit factor through which age may affect advice, such as renal function, pregnancy status, frailty, medication use, or screening history.

This experiment asks whether a model uses chronological age as a crude proxy when the clinically relevant factor is available. It could become the paper's most novel analysis, but it should be attempted only after the main benchmark and human rubric are working. A large embedding or mechanistic study is lower priority within the two-month window.

## Recommended technical architecture

Use a regular **Python project as the source of truth**. Jupyter or Google Colab should be a thin interface for exploration, GPU pilots, and final figures—not the place where pipeline state, manual data copying, or primary analysis lives. C++ is unnecessary unless the project later develops custom inference kernels.

| Need | Recommended technology |
|---|---|
| Language/environment | Python 3.11; `uv`; `pyproject.toml`; committed `uv.lock` |
| Core structure | Installable `src/age_eval/` package plus small command-line entry points |
| Tabular data | Pandas and PyArrow; versioned Parquet for tables and JSONL for raw API records |
| Schemas/validation | Pydantic for request/response records; Pandera or explicit schema tests for dataframes |
| Configuration | Versioned YAML files for datasets, models, prompts, decoding, and evaluation rubrics |
| Closed-model inference | Official provider SDKs and batch APIs; retries, raw-response retention, and stable request IDs |
| Open-model inference | Hugging Face Transformers for development; vLLM for batched GPU inference when supported |
| Annotation | Institution-approved REDCap if available; otherwise self-hosted Label Studio on approved storage |
| Statistics | NumPy, pandas, SciPy, statsmodels, and scikit-learn; cluster bootstrap implemented as tested Python code |
| Quality controls | pytest, Ruff, schema checks, and a small GitHub Actions workflow |
| Provenance | SHA-256 file manifests, Git commit/model IDs, prompt hashes, run IDs, timestamps, and cost/token logs |
| Reproduction | A minimal Docker image after the pilot; one command to rebuild tables and figures from frozen inputs |
| Notebooks | At most a few notebooks for EDA, pilot review, and figures; import all logic from `src/age_eval/` |

Suggested repository shape:

```text
age-llm-medical-evaluation/
├── pyproject.toml
├── uv.lock
├── configs/
├── src/age_eval/
│   ├── data/
│   ├── generation/
│   ├── evaluation/
│   └── analysis/
├── tests/
├── notebooks/
├── artifacts/manifests/
└── docs/
```

## Compute recommendation

- A laptop is sufficient for dataset preparation, API-based generation, validation, statistics, and writing.
- Use Colab only for early open-model experiments if no institutional GPU is available.
- Use an institutional GPU cluster or dedicated cloud instance for the full open-weight run, because the hardware and runtime should be recorded and the job must be resumable.
- Store every batch result outside the ephemeral compute environment immediately; a failed job must resume by stable request ID rather than row position.

## Practical priority order

1. Finalize schemas, question inclusion rules, and the 100-case pilot.
2. Obtain early clinician review and refine the rubric.
3. Build and test the Python pipeline on one model.
4. Run the multi-model pilot and freeze the protocol.
5. Create the human gold set and evaluate judge reliability.
6. Run the full benchmark and primary analysis.
7. Add mitigation and the mediator challenge set only if the core gates pass.

Do not spend the first weeks porting notebooks, writing C++, adding dashboards, or scaling to thousands of cases. The strongest paper comes from a valid construct, a clean gold set, and traceable paired evidence.
