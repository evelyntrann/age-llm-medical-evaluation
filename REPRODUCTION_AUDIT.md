# Reproduction and Research-Validity Audit

**Audit date:** September 2, 2026  
**Scope:** repository at commit `a434a13c`, the included thesis, all six notebooks, both metric modules, committed data/results, the public repository and dataset pages, and the MLHC 2026 reviews supplied by the researcher.

## Executive finding

The scientific question is strong, but the released artifacts do not support the paper's current causal, safety, or mechanistic claims. The safest path is a clean rebuild with the old work retained as a documented pilot. Do not quote the legacy result numbers in a new paper unless the raw records are recovered, joined by stable IDs, and reproduced end to end.

## Critical blockers

### 1. The counterfactual intervention does not isolate age

- The generation prompt asks Qwen to add age-specific phrasing, symptoms, duration, and concerns. It therefore changes clinical content as well as age.
- Direct inspection shows variants adding different symptoms and histories to the same base question.
- The committed generated table has 53,585 rows (10,717 per label), whereas the paper reports 53,395 (10,679 per label).
- Semantic pairing becomes shifted at zero-based group 4,055: an age variant belongs to the following scenario, and the corruption continues afterward.
- There are duplicated prompts, already age-specific baselines, third-person/caregiver cases, pregnancy/child cases, and nonmedical questions.

**Consequence:** observed response differences cannot be attributed to age.

### 2. Response-to-prompt lineage is unsafe

- The GPT batch notebook assigns returned records by file order and does not join them using `custom_id`; skipped or malformed lines can shift all later answers.
- The Llama notebook uses a different system instruction and token limit, then exports a reduced schema that does not match downstream expectations.
- Notebooks mix local files, remote mutable datasets, manual copy steps, and stale cell outputs.
- Raw keyed response and audit files needed to reconstruct the reported figures are absent from the repository.

**Consequence:** the released outputs cannot be proven to correspond to their intended prompts.

### 3. Safety labels are not clinically validated

- A single MedGemma configuration supplies both safety and severity judgments.
- The judge receives only the generated answer, not the patient's question or clinical context.
- Free-form judge outputs are not schema-constrained or robustly parsed.
- Severity is requested for every safety output other than exactly `1`, although the rubric defines unsafe responses at a higher threshold.
- In metric code, invalid baseline safety values default to `2`, while invalid age-conditioned values default to `3`; this mechanically biases the comparison.
- The public audit dataset visibly contains nonnumeric, verbose judge outputs in fields treated as scores.

**Consequence:** the safety endpoint is confounded by evaluator behavior and parsing defaults.

### 4. Reported analyses conflict with code and artifacts

- Saved GPT results report 4,326 defaulted values and an impossible senior mean safety value of `901.9441`.
- ADSB sign interpretations conflict across code, text, and figures.
- The metrics notebook shows 1,199 comparisons per group in some cells, while saved results use 10,679.
- Group membership is inferred from every five adjacent rows rather than a validated scenario key.
- Tone disparity uses ad hoc keyword and substring counts; terms such as “older adults” are treated as patronizing regardless of context, and absolute differences erase direction.

**Consequence:** current tables and figures should not be treated as verified results.

### 5. The embedding study is descriptive, incomplete, and internally inconsistent

- Mean pooling includes padding tokens even though the paper states attention-mask-weighted pooling.
- Prompts are truncated at 256 tokens without a reported sensitivity analysis.
- “Agency” and “competence” directions come from a small hand-selected word list, are nearly collinear, and are not validated on held-out terms.
- Embedded notebook outputs imply only 5,340 age rows were processed where the claimed design requires tens of thousands; layer summaries are implausibly identical.
- Projections of prompt embeddings are associations, not evidence of a model's causal mechanism.

**Consequence:** mechanistic claims should be removed from the core paper; a redesigned representation study can be future work.

## Review synthesis

The MLHC meta-review and reviewers converge on five issues:

1. Appropriate age adaptation is not distinguished from unfair bias.
2. The auxiliary rewriting process breaks the counterfactual design.
3. The sole LLM judge lacks clinician calibration and could itself be age-biased.
4. The proposed safety, severity, and tone metrics are ad hoc or overinterpreted.
5. Claimed mitigation and mechanistic contributions are absent or substantially overstated.

One clinical reviewer considered the topic relevant and potentially useful, but still questioned human validation, reproducibility, and clinical significance. This supports rebuilding the study, not abandoning the question.

## Required remediation before new claims

- Construct age-only, keyed counterfactuals and validate every pair for content equivalence.
- Define appropriate, neutral, and inappropriate adaptation with clinician-authored criteria.
- Use two independent clinical raters, adjudication, and agreement reporting on a powered stratified subset.
- Calibrate any LLM judge to the gold set and separately test judge age sensitivity.
- Freeze exact model snapshots, prompts, settings, dataset hashes, and analysis decisions.
- Replace silent coercion/defaults with schema validation, retries, explicit missingness, and failure reports.
- Use paired effect sizes and confidence intervals; reserve tone and embeddings for secondary/exploratory analysis.
- Include a mitigation experiment only if it tests the central clinical tradeoff.
- Reproduce all figures and tables from a clean environment before submission.

## Artifact-specific notes

- `data/base_prompts.csv`: 3,160 rows, 3,152 unique question texts.
- `data/gen_prompts.csv`: 53,585 rows; 10,717 rows per age label; 10,268 unique baseline texts; only 2,948 unique baseline texts overlap the base CSV.
- `01_prompt_generation.ipynb`: current code and embedded outputs disagree on dataset size and augmentation model.
- `02_gpt_batch_inference.ipynb`: partial 6,000-row output shown; order-based response assignment.
- `03_llama_inference.ipynb`: prompt/configuration and output-schema mismatch.
- `04_medgemma.ipynb`: context-free, unconstrained evaluator; incomplete embedded run.
- `05_embeddings.ipynb`: missing expected audit file and invalid pooling/interpretation.
- `06_metrics.ipynb`: mixed run sizes and environment mutation inside the analysis.
- `requirements.txt`: environment dump with platform-specific and unrelated dependencies, not a portable project lock.
- Repository: no tests, continuous integration, release tag, data manifest, or complete raw-result package.

## Recommended disposition

Archive the current pipeline under a clearly marked `legacy/` area only after all recoverable raw artifacts have been inventoried. Build the new benchmark, generation, evaluation, and analysis pipeline alongside it with immutable IDs and manifests. Preserve provenance; do not delete the original files during the rebuild.
