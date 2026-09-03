# Evidence Review and Conference-Standard Reassessment

**Review date:** September 2, 2026  
**Scope:** targeted narrative review of peer-reviewed research, consensus reporting guidance, and official conference criteria. This is not a systematic review; searches were designed to test the proposal's assumptions and novelty.

## Bottom line

The revised project is scientifically preferable to the inherited study, but the earlier two-page proposal was not yet conference-competitive. It repaired the old experiment without sufficiently accounting for adjacent work published by 2024-2026. Its significance and basic direction were strong; originality, clinical-rater design, power for rare harms, age-stratum justification, and FAccT sociotechnical fit remained incomplete.

The evidence supports a further reframing from “age bias in medical answers” to **calibrated reliance on age**. The paper should measure both over-conditioning and under-conditioning, use prospectively specified clinical expectations, combine representative and challenge datasets without pooling their prevalence, and treat automated judges as selectively validated secondary instruments.

## What the literature establishes

| Evidence | Relevant result | Consequence for this project |
|---|---|---|
| [Wang et al., ACL 2025, Best Paper](https://aclanthology.org/2025.acl-long.341/) | Fairness may require contextually appropriate group differentiation; standard “difference-unaware” mitigation can backfire. | The main construct must be appropriate versus inappropriate age use, not response equality. |
| [EquityMedQA, Nature Medicine](https://www.nature.com/articles/s41591-024-03258-2) | Used participatory rubric design, independent/pairwise/counterfactual tasks, 4,619 examples, and 17,099 human ratings; rater groups differed and agreement could be modest or poor. | Use both individual-answer and paired ratings, multiple perspectives, pilot training, agreement analysis, and transparent disagreement. |
| [HealthBench](https://openai.com/index/healthbench/) | Uses 5,000 health conversations and 48,562 physician-written, scenario-specific criteria; model grading is meta-evaluated against physicians. | Generic 1-5 safety scales are too coarse; use case-specific criteria and validate the grader. This is an industry benchmark, so it is a design precedent rather than independent clinical authority. |
| [Adaptive Precise Boolean rubrics, npj Digital Medicine 2026](https://www.nature.com/articles/s41746-026-02492-x) | Granular Boolean criteria increased inter-rater agreement and took about half the evaluation time of Likert rubrics in the studied domain. | Replace the single global safety score with precise yes/no criteria where feasible. |
| [Human evaluation framework, npj Digital Medicine 2024](https://www.nature.com/articles/s41746-024-01258-7) | Recommends explicit use cases, success criteria, evaluator training, blinding, agreement measurement, and larger evaluator panels; suggests four evaluators for medical research applications. | Two clinicians are a minimum feasibility design, not a strong target. Recruit three to four and double-rate every gold item. |
| [Williams et al., npj Digital Medicine 2026](https://pubmed.ncbi.nlm.nih.gov/42477479/) | Among five LLM judges versus six clinicians, the best judge matched humans on only four of eleven criteria; a judge jury improved only one additional criterion. | Multiple judges do not automatically solve validity. Validate per criterion and retain human evaluation as primary. |
| [Zheng et al., NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html) | LLM judges can exhibit position, verbosity, self-enhancement, and reasoning biases. | Include response-order, verbosity, self-judge, and age-label controls. |
| [Framework for bias evaluation in healthcare LLMs, npj Digital Medicine 2025](https://www.nature.com/articles/s41746-025-01786-w) | Proposes stakeholder engagement, power calculations, clinically relevant scenarios, randomized demographic factors, automated audits, and context-specific clinical interpretation. | Predefine clinically important effects, randomize conditions, power the study, and engage affected stakeholders. |
| [MedEinst, ACL 2026](https://aclanthology.org/2026.acl-long.1847/) | Built 5,383 counterfactual paired medical cases around a specific failure mechanism and evaluated a mitigation. | “Paired medical benchmark plus mitigation” is no longer novel by itself; age-reliance calibration and mediator tests must carry the novelty. |
| [Age-related performance in genetic conditions, npj Aging 2025](https://www.nature.com/articles/s41514-025-00226-z) | Evaluated age-related differences in vignettes, dialogues, and management plans across genetic conditions and found that some age differences were clinically expected. | The related-work section must acknowledge prior age-specific medical LLM evaluation and justify a broader patient-advice task. |
| [CHART reporting guideline, BMJ 2025](https://www.bmj.com/content/390/bmj-2024-083305) | Consensus checklist covers use case, ground truth, model/version/date, prompts, query strategy, sample size, analysis, response data, and open science. | Use CHART from protocol design onward, not merely when writing the paper. |
| [WHO ageism-in-AI policy brief](https://www.who.int/publications/i/item/9789240040793) | Recommends participatory design with older people, age-inclusive data, governance, consent/contestability, and robust ethics. | A FAccT paper about ageism should include older-adult stakeholder input or explicitly narrow claims to clinical response behavior. |
| [The two faces of elderspeak, npj Dementia 2026](https://www.nature.com/articles/s44400-026-00072-0) | Age-adapted communication can help or harm depending on the feature and context. | Do not label simpler or warmer language as inherently patronizing; communication harm needs patient-centered validation. |

## Novelty assessment

The following claims are **not sufficient as primary novelty**:

- adding demographic labels to prompts and comparing outputs;
- releasing another large medical question set;
- using an LLM judge plus a small clinician spot-check;
- showing that models differ across age groups;
- proposing a prompt mitigation without testing preservation of beneficial adaptation; or
- projecting embeddings onto hand-selected “agency” or “competence” directions.

A defensible novelty claim is:

> We introduce a clinician-specified, two-sided evaluation of calibrated age reliance in patient-facing medical advice, distinguishing over-conditioning from under-conditioning and testing whether explicit clinical mediators reduce inappropriate reliance on chronological age.

This combines ideas found separately in difference-aware fairness, clinical counterfactual evaluation, and personalized health rubrics, but applies them to a specific unresolved problem with a new two-sided task and validation design.

## Conference-style review of the earlier proposal

### Significance: strong

Age is clinically relevant and a potential source of stereotyping. The problem affects patient-facing systems and can yield actionable audit and mitigation results.

### Relevance: strong for CHIL/MLHC; conditional for FAccT

[CHIL's official criteria](https://chil.ahli.cc/submit/call-for-papers/) emphasize relevance, technical quality, originality, clarity, significance, and reproducibility. [MLHC](https://mlhc.org/paper-submission) asks for important, generalizable insights and explicitly welcomes benchmarks, equity work, and replication. The revised study fits those venues if it yields a reusable evaluation construct rather than a model leaderboard.

[FAccT's 2027 criteria](https://facctconference.org/2027/authorguide.html) emphasize rigor, originality, impact, limitations, and holistic sociotechnical analysis. Its call states that work without deep engagement with social components may be out of scope. A clinician-only technical benchmark is therefore a borderline fit; meaningful older-adult/patient or health-equity involvement would materially improve relevance.

### Originality: borderline in the earlier plan

EquityMedQA, Fairness through Difference Awareness, recent clinical bias-audit frameworks, and MedEinst occupy much of the surrounding space. The original plan's “age-only pairs plus clinicians plus mitigation” would likely be judged incremental unless the calibrated-reliance construct and mediator experiment are central.

### Construct validity: conditional

The plan correctly moved to deterministic age insertion, but exact ages such as 16, 30, 50, and 75 were illustrative rather than clinically justified. Pediatric versus adult care is a major regime change, not merely another age group. Adult anchors should be justified, and pediatric cases should be a separate analysis if retained. Naturalistic questions often omit needed context, so appropriate context-seeking must be an outcome rather than an automatic failure.

### Human evaluation: below strong-conference standard as originally written

Two clinicians across broad specialties are unlikely to establish stable clinical ground truth. A stronger feasible design uses three to four clinicians, two independent ratings per item, triple-rating on a prespecified subset, adjudication, rater training, and domain matching. Communication or ageism judgments require a patient/older-adult or health-equity perspective if claimed.

### Automated evaluation: needs stricter limits

Testing two judge families is not enough. Validation must be criterion-specific and held out, with uncertainty and bias controls. Automated labels should scale only criteria with adequate sensitivity and specificity; they should not replace the human primary endpoint.

### Statistics: incomplete in the earlier plan

“At least 400 pairs” was not evidence-based. Rare harmful events and model-by-age subgroups may be underpowered even when 400 pairs suffice for aggregate agreement. The final design needs a minimum clinically important effect, pilot-based or simulation-based power, scenario-level clustering, rater effects, multiplicity control, and separate reporting for representative versus adversarial samples.

### Reproducibility and reporting: strong direction, not yet implemented

Stable identifiers, raw-response retention, frozen model snapshots, manifests, schema validation, tests, and clean rebuilds directly address the inherited failures. The CHART checklist should become a protocol checklist. The final repository must demonstrate these properties rather than promise them.

### Provisional overall judgment

If the earlier plan were executed exactly as written, I would expect a **borderline-to-reject** review because the novelty and clinical validation could still be challenged. If the evidence-based V2 is executed with adequate clinician/stakeholder participation, prespecified power, a clean held-out evaluation, and transparent negative results, it becomes plausibly competitive. No responsible acceptance probability can be assigned before the pilot and results.

## Required protocol changes

1. Fix the target use case as patient-facing health advice.
2. Justify adult age anchors and separate pediatric analysis.
3. Build two datasets: representative naturalistic questions and an enriched clinician challenge set; never pool prevalence.
4. Have clinicians specify expected response invariance/adaptation before seeing outputs.
5. Use three to four clinicians, at least two ratings per gold item, and adjudication.
6. Use precise, case-specific Boolean criteria plus independent and paired assessment.
7. Power primary endpoints from a clinically important effect and estimated clustering; enrich rare failures without calling the enriched rate prevalence.
8. Measure generation variability on repeated queries.
9. Validate LLM judges by criterion on held-out human ratings and route uncertain cases to humans.
10. Add an age-relevance mitigation and, if feasible, a clinical-mediator factorial test.
11. Add older-adult/patient or health-equity participation for FAccT; otherwise prefer CHIL/MLHC.
12. Design and report the study using CHART and the target conference's ethics/reproducibility rules.

## Go/no-go conditions before full generation

- Advisor approves the use case, age strata, primary outcomes, venue, and contribution claim.
- Data licenses and institutional IRB/human-participant determination are documented.
- At least three clinicians are committed, or scope is narrowed enough for qualified domain coverage.
- Pilot rubric agreement is interpretable and revision rules are frozen before the held-out evaluation.
- Power simulation supports the planned confirmatory analyses.
- The 100-case pilot has zero pair-content corruption and zero untracked parse failures.
- Automated evaluator thresholds and human fallback rules are prespecified.
- Compute and annotation budgets are sufficient for the frozen design.

## Publication-policy note

The FAccT 2027 author guide currently requires a generative-AI usage statement and prohibits using LLMs to generate publication text, while allowing limited formatting or grammar assistance with disclosure. The researcher must author the eventual FAccT manuscript and verify every citation. The present AI-assisted planning and literature triage should not be copied directly into a FAccT submission as manuscript prose.
