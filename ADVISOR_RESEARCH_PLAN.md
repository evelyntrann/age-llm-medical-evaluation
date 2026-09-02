# Two-Month Research Plan: Clinically Calibrated Auditing of Age-Conditioned Medical Advice

**Project window:** September 2-November 3, 2026  
**September milestone:** approved protocol, validated pilot, and submission decision by September 30  
**Primary venue under consideration:** ACM FAccT 2027 (abstract October 27; paper November 3), with CHIL/MLHC 2027 as a fallback if the validation is not mature

## Motivation and revised scope

The inherited project asks an important question: does adding patient age cause language models to change medical advice in ways that help or harm patients? The prior MLHC submission was rejected because the study did not separate medically appropriate age adaptation from unfair differential treatment, relied on a single unvalidated LLM judge, used an age-generation process that also changed symptoms and clinical facts, and overstated preliminary linguistic and embedding analyses.

A forensic audit also found that the released prompts and outputs do not reliably reproduce the paper: the prompt table contains 53,585 rather than 53,395 rows; scenario alignment becomes corrupted; model prompts and generation settings differ; invalid judge outputs are silently replaced with asymmetric defaults; and several saved results conflict with notebook outputs. Therefore, I propose a clean, preregistered rebuild. The legacy study will be documented as pilot work, but none of its numerical findings will be reused unless reconstructed from raw, keyed records.

## Objective and research questions

The objective is to build a clinically grounded counterfactual benchmark that measures when age conditioning produces appropriate adaptation, no meaningful change, or inappropriate clinical change.

1. Holding the clinical scenario constant, how often does an exact patient age change an LLM's recommendation?
2. When age changes an answer, is the change clinically appropriate, neutral, unnecessarily stereotyped, or potentially harmful?
3. Do automated evaluators reproduce clinician judgments, and are the evaluators themselves sensitive to age labels?
4. Which model and scenario characteristics predict inappropriate age-conditioned changes?
5. Can a simple instruction-based mitigation reduce inappropriate changes without suppressing beneficial age adaptation?

## Study design

**Benchmark.** Curate 800-1,000 first-person medical scenarios from sources with verified licenses. Remove nonmedical items, caregiver/third-person questions, explicit-age cases, duplicates, protected health information, and cases whose facts cannot be held constant. Clinicians will classify scenarios as age-invariant, age-relevant, or age-conditional and stratify them by specialty and acuity. Each retained scenario will receive a neutral condition and deterministic exact-age variants (for example, 16, 30, 50, and 75 years). Only the age sentence will change; an LLM will not rewrite symptoms, duration, or history. A small secondary experiment may compare numeric ages with labels such as “older adult.”

**Models and generation.** Evaluate four defensible model families: a frontier general model, a smaller production-oriented model, an open-weight general model, and a medically tuned model. Exact model snapshots, access dates, system prompts, decoding settings, and response hashes will be frozen before the full run. The same task instruction and comparable decoding configuration will be used wherever APIs permit. Models from the prior paper may be included only as a historical appendix.

**Primary outcome.** The unit of analysis is a paired neutral-versus-aged response for the same scenario and model. The primary endpoint is an *inappropriate age-conditioned clinical change*. Prespecified failure categories are unsafe action, under-triage, over-triage, omitted warning or escalation, unsupported certainty, unsupported age-based assumption, and refusal/irrelevance. Appropriate prevention, dosing, differential diagnosis, communication, or escalation changes will be labeled beneficial rather than biased. Equivalent answers form the no-material-change category.

**Human and automated evaluation.** Two independent clinically qualified raters will score a stratified sample of at least 400 paired comparisons, with the final sample size set from the pilot and balanced across models, age strata, relevance classes, and acuity. Raters will be blinded to model identity and study hypotheses where possible; disagreements will be adjudicated. Agreement and uncertainty will be reported. Two distinct LLM-judge families may scale the remaining evaluation only after calibration against the human set. Judges will see the original scenario and response, use constrained categorical outputs, and be tested with age-swapped but otherwise identical inputs. If agreement is inadequate, automated scores will remain secondary.

**Analysis.** Report paired absolute risk differences with cluster-bootstrap confidence intervals, plus a mixed-effects model with scenario-level random intercepts. Emphasize effect sizes and clinically important failure modes rather than significance alone. Analyze age-relevance and acuity strata separately. Readability and tone are secondary descriptive outcomes; the current Tone Disparity Index will not support clinical-harm claims. Embedding projections are optional exploratory work only after the clinical study is complete and may not be described as a causal mechanism.

**Mitigation.** On the strongest and weakest model, test one prespecified system instruction that requires age to affect advice only through clinically relevant factors and requires uncertainty or clarification when those factors are absent. Success means fewer inappropriate changes without a meaningful loss of appropriate adaptations or overall safety.

## Eight-week execution plan

| Week | Dates | Work and decision point |
|---|---|---|
| 1 | Sep 2-8 | Finish artifact audit; recover raw outputs if available; define data lineage, versioned schemas, and exclusion rules. |
| 2 | Sep 9-15 | Build and manually QA a 100-scenario benchmark; draft annotation rubric; obtain license/privacy/IRB determination and clinician commitments. |
| 3 | Sep 16-22 | Run a 100-200-scenario, 3-4-model pilot; estimate failure prevalence, cost, rater time, and judge reliability. |
| 4 | Sep 23-30 | Calibrate raters and judges; freeze models, prompts, sample size, endpoints, exclusions, and analysis. Advisor go/no-go review. |
| 5 | Oct 1-7 | Generate the full benchmark and model responses with keyed manifests, validation checks, and resumable pipelines. |
| 6 | Oct 8-14 | Complete human annotation and calibrated automated evaluation; run the primary paired analysis. |
| 7 | Oct 15-21 | Run mitigation, robustness checks, subgroup analysis, and qualitative error analysis. Submission-quality go/no-go by Oct 20. |
| 8 | Oct 22-Nov 3 | Write paper and limitations; package code, data statements, model cards, audit samples, and reproducibility instructions. |

## Success gates and deliverables

The study advances only if: every response is joined by stable IDs; benchmark QA detects no clinical-content drift; parsing has no silent defaults; clinician review is available; evaluator validity meets a threshold fixed after the pilot; and a clean environment can reproduce tables and figures from manifests. If clinician validation or evaluator reliability is insufficient by September 30, I will not make clinical-safety claims and will move the submission to CHIL/MLHC 2027 rather than rush it.

Deliverables are a versioned counterfactual benchmark, clinician-authored rubric and adjudicated gold set, reproducible multi-model evaluation pipeline, paired statistical analysis, mitigation experiment, documented limitations, and a release-ready paper repository.

## Decisions requested from the advisor

1. Approve the revised framing and permission to treat the prior results as pilot-only.
2. Identify two clinical raters and an adjudicator, or approve a budget to recruit them.
3. Approve the API/GPU and annotation budget after the Week 3 pilot.
4. Confirm data-governance/IRB requirements, authorship responsibilities, and FAccT 2027 as the conditional primary target.
