# Research Continuation Proposal

## Calibrated Age Reliance in Patient-Facing Medical Advice from Large Language Models

**Project period:** September 2-November 3, 2026  
**Purpose:** First detailed planning meeting with advisor  
**Researcher:** [Name]

### Motivation and research gap

Age can legitimately affect differential diagnosis, screening, medication risk, urgency, and communication. Therefore, equal wording across ages is not necessarily fair, and different wording is not necessarily biased. The scientific problem is whether a model uses age **when, where, and in the direction clinically warranted**.

The inherited project established a useful pilot, but the reviews and reproduction audit identified confounded age manipulations, corrupted pairing, incomplete provenance, dependence on one unvalidated LLM judge, and overinterpretation of tone and embeddings. I propose rebuilding the core experiment rather than extending its numerical results.

Recent work makes a simple demographic-swap audit insufficiently novel. EquityMedQA already uses independent, pairwise, and counterfactual health-equity evaluation; Fairness through Difference Awareness formalizes contextually appropriate group differentiation; and newer medical benchmarks use physician-authored criteria. The proposed contribution is therefore a narrower construct: **calibration of age reliance**, measured as both inappropriate reliance on age and failure to use age when clinically necessary.

### Research questions

1. When clinical facts are held constant, do models remain invariant when age should not matter and adapt appropriately when it should?
2. What are the rates of over-conditioning, under-conditioning, appropriate adaptation, and harmful adaptation?
3. How do these rates vary across model families, age conditions, clinical domains, and case acuity?
4. Can automated evaluators reproduce criterion-level clinician judgments without adding age, position, or verbosity bias?
5. Can an age-relevance prompting intervention reduce over-conditioning without increasing under-conditioning or reducing overall safety?

### Proposed study

**Use case and benchmark.** The primary use case will be patient-facing general health advice, not autonomous diagnosis or clinician decision support. I propose two complementary datasets:

- a representative set of approximately 300-500 licensed, naturalistic health questions for estimating ordinary model behavior; and
- a challenge set of approximately 100-150 clinician-authored or clinician-refined cases, balanced across age-invariant, age-relevant, and age-conditional situations.

The two sets will be analyzed separately so that enrichment for difficult cases is not mistaken for real-world prevalence. A smaller gold core is preferable to a larger noisy benchmark.

Each scenario will receive an age-unspecified condition and exact-age conditions through deterministic insertion only. Symptoms, history, duration, and concerns will not be rewritten. Adult anchor ages will be selected with clinical justification; pediatric cases will either be excluded from the primary analysis or treated as a separate prespecified stratum. Before model generation, clinicians will record whether age should matter, which response components should remain invariant or change, and the clinically appropriate direction. Every question, condition, response, and rating will have immutable identifiers and provenance.

**Models and generation.** Evaluate four complementary model categories: a frontier general model, a smaller production model, an open-weight model, and a medically tuned model. Exact snapshots, access dates, system prompts, sampling settings, and response hashes will be frozen. A repeated-generation subset will estimate within-model variability so that sampling noise is not interpreted as an age effect.

**Human evaluation.** Use a panel of three to four clinically qualified raters matched as closely as possible to the benchmark's domains. Each gold item will receive at least two independent ratings; a prespecified subset will be triple-rated, and disagreements will be adjudicated. Raters will be trained on pilot examples and blinded to model identity. They will first assess each answer independently and then compare the age-paired answers.

Use scenario-specific, precise Boolean criteria where possible—for example, whether emergency escalation was included when required—rather than relying mainly on a global 1-5 safety score. Report agreement with confidence intervals and preserve disagreement rather than hiding it behind majority vote. If communication, patronization, or elderspeak remains a substantive outcome, include an older-adult/patient or health-equity perspective in rubric development; clinicians alone cannot establish perceived communication harm.

**Automated evaluation.** LLM judges will be secondary. Candidate judges will receive the question, age condition, response, and precise rubric. Their criterion-level sensitivity, specificity, and agreement with clinicians will be estimated on held-out ratings, including age-swapped, response-order-swapped, and verbosity controls. Automated ratings will be used only for criteria that pass thresholds fixed after the pilot; uncertain or discordant cases will remain human-reviewed.

**Outcomes and analysis.** Co-primary endpoints are over-conditioning and under-conditioning. Harmful and appropriate adaptation, independent response safety, and context-seeking are secondary clinical outcomes. The protocol will define a minimum clinically important difference and use pilot-based simulation to choose sample size. Report paired absolute risk differences and 95% confidence intervals, cluster resampling by scenario, and a mixed-effects model accounting for scenario and rater. Confirmatory hypotheses will be separated from exploratory subgroup analyses, with multiplicity control.

**Mitigation and stretch experiment.** The core mitigation will ask the model to identify whether age is clinically relevant before composing advice. Success requires reducing over-conditioning while preserving necessary adaptation and absolute safety. If the core study passes its quality gates, add a small four-condition mediator experiment—neither age nor mediator, age only, mediator only, and both—to test whether models use chronological age as a crude proxy for factors such as renal function, frailty, medication use, or screening history.

### Eight-week execution and decision gates

| Period | Deliverable and gate |
|---|---|
| Sep 2-8 | Complete artifact inventory, literature map, use-case definition, data schema, and provenance rules. |
| Sep 9-15 | Construct and validate a 100-case pilot; draft precise clinical rubrics; obtain data-license and IRB determination. |
| Sep 16-22 | Run the multi-model pilot; estimate event rates, generation variability, annotation time, and judge validity. |
| Sep 23-30 | Calibrate raters; define clinically important effects; run power simulation; freeze endpoints, models, prompts, exclusions, and analysis. |
| Oct 1-14 | Generate frozen benchmark responses and complete the prespecified human gold evaluation. |
| Oct 15-21 | Run primary analysis, robustness controls, mitigation, and qualitative failure analysis. |
| Oct 22-Nov 3 | Write and reproduce the paper; release allowable data, rubrics, code, manifests, and reporting checklist. |

The study proceeds only if counterfactual content is valid, clinician agreement is interpretable, primary outcomes are adequately powered, evaluator failures are explicit, and results regenerate from frozen inputs. The challenge set and representative set must never be pooled for prevalence estimates.

### Venue and decisions requested

CHIL or MLHC is the natural fit for a clinically centered benchmark and evaluation paper. FAccT 2027 remains possible only if the study adds meaningful patient/older-adult or health-equity stakeholder engagement and a deeper sociotechnical analysis; otherwise the work risks being viewed as a purely technical audit.

I request guidance on: (1) the patient-facing scope and age strata; (2) access to three or four clinicians and, if targeting FAccT, an older-adult/patient or health-equity advisor; (3) annotation and compute budget; (4) IRB, consent, compensation, privacy, and licensing requirements; (5) the minimum clinically important difference; and (6) venue, authorship, and publication schedule.
