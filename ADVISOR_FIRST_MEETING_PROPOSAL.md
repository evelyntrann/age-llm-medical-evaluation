# Research Continuation Proposal

> **Superseded after literature review.** Use `ADVISOR_FIRST_MEETING_PROPOSAL_V2.md` for the advisor meeting. This version is retained for comparison.

## When Should Age Matter? Clinically Calibrated Evaluation of Age-Conditioned Medical Advice from Large Language Models

**Proposed project period:** September 2-November 3, 2026  
**Prepared for:** First project-planning meeting with advisor  
**Researcher:** [Name]

### 1. Background and motivation

Large language models are increasingly used to answer health questions, but their advice may change when a patient's age is included. Some changes are medically necessary: age can affect differential diagnosis, medication risk, screening, urgency, and communication. Other changes may be unsupported, stereotyped, overly reassuring, or unsafe. Therefore, measuring whether answers merely differ by age is insufficient. The important question is whether the difference is **clinically justified**.

The inherited project established a useful starting point and assembled an age-focused evaluation pipeline. However, the conference reviews and my preliminary reproduction audit identify limitations that prevent the existing results from supporting strong conclusions. The generated age variants sometimes change symptoms and context in addition to age; parts of the dataset lose correct scenario alignment; response and evaluator records are not consistently linked by stable identifiers; the safety scores rely on one unvalidated LLM judge; and the linguistic and embedding analyses are interpreted more strongly than the evidence supports.

I propose retaining the previous work as a documented pilot while rebuilding the core experiment with controlled counterfactuals, clinical validation, paired statistics, and complete data provenance.

### 2. Objective and research questions

The objective is to determine when age conditioning improves medical advice and when it causes inappropriate or harmful differences. The design captures two complementary failures: **over-conditioning**, where age changes advice without clinical justification, and **under-conditioning**, where a model fails to adapt when age should matter.

1. Does a model remain invariant when age should not matter and adapt appropriately when it should?
2. What are its rates of over-conditioning, under-conditioning, and harmful adaptation?
3. How do inappropriate changes vary across model families, patient ages, clinical domains, and case acuity?
4. Can automated evaluators reproduce clinician judgments without introducing their own age-related bias?
5. Can a simple prompting intervention reduce inappropriate changes without suppressing beneficial adaptation?

### 3. Proposed methodology

**Controlled benchmark.** I will curate a candidate pool of up to 1,000 first-person medical scenarios from sources with verified licenses, prioritizing a smaller, high-quality core over raw scale. I will remove duplicates, nonmedical questions, already age-specific cases, third-person/caregiver questions, and cases whose clinical facts cannot remain constant. Scenarios will be stratified by clinical domain, acuity, and expected age relevance: age-invariant, age-relevant, or age-conditional.

Each scenario will have one age-unspecified version and four exact-age versions—for example, ages 16, 30, 50, and 75. The transformation will be deterministic: only a short age statement will be inserted. No model will rewrite symptoms, duration, history, or patient concerns. Every prompt will have an immutable scenario and condition identifier.

I will prepare and quality-check the candidate questions first. Before full-scale generation, a clinician will review the 100-case pilot, age-relevance labels, acuity labels, and scoring rubric. For the clinician-validated core, the reviewer will also specify which response dimensions should remain invariant or adapt with age. This early checkpoint prevents generating thousands of answers from clinically unsuitable questions; clinicians do not need to write or review every item in the extended dataset.

**Model evaluation.** I propose evaluating four complementary model categories: a frontier general model, a smaller production-oriented model, an open-weight general model, and a medically tuned model. Exact model versions will be selected after checking access and cost, then frozen before the main experiment. Prompts, decoding settings, access dates, and response hashes will be recorded. A 100-200-scenario pilot will determine feasibility and final sample size before the full run.

**Clinical outcome rubric.** The co-primary endpoints will be the rates of **over-conditioning** and **under-conditioning** within paired responses. Harmful age-conditioned change will be reported separately. The rubric will distinguish:

- appropriate adaptation, such as justified changes to screening, differential diagnosis, treatment risk, or escalation;
- no clinically meaningful change;
- unsupported age assumptions or stereotyping;
- under-triage, over-triage, omitted warning or escalation, unsafe action, or unsupported certainty; and
- refusal, irrelevance, or other response failures.

Tone and readability will be secondary descriptive outcomes. They will not be treated as evidence of clinical harm by themselves. Embedding analysis will be optional exploratory work after the primary clinical evaluation and will not be presented as a causal mechanism.

**Human and automated evaluation.** After answers are generated, two clinically qualified raters will independently evaluate a stratified sample of at least 400 paired comparisons—not the entire model-output dataset. They will first score each answer's clinical quality and then judge whether the between-age difference is appropriate. The final number will be based on pilot prevalence and workload. Model identity will be hidden where possible, disagreements will be adjudicated, and inter-rater agreement will be reported.

Automated evaluation may be used for scale only after comparison with the human gold set. I will test two independent judge-model families, provide each judge with both the original question and response, require structured outputs, and test whether age labels change the judge's score when answer content is held constant. If judge agreement with clinicians is insufficient, automated findings will remain secondary.

**Statistical analysis and mitigation.** I will report paired absolute risk differences with confidence intervals, supported by cluster bootstrapping and mixed-effects models with scenario-level random effects. Analyses will be stratified by age relevance and acuity, emphasizing effect sizes and clinically meaningful errors rather than significance alone. Finally, I will test one prespecified system instruction that asks models to use age only when medically relevant and to state uncertainty when necessary. A successful mitigation must reduce inappropriate changes without reducing appropriate adaptation or overall safety.

### 4. Eight-week work plan

| Period | Milestone |
|---|---|
| Sep 2-8 | Complete artifact inventory; define data schema, provenance, inclusion criteria, and recoverable legacy materials. |
| Sep 9-15 | Build and manually verify a 100-scenario benchmark; draft the clinician rubric; obtain license/privacy/IRB guidance. |
| Sep 16-22 | Run the multi-model pilot; estimate costs, failure prevalence, rater workload, and evaluator reliability. |
| Sep 23-30 | Calibrate raters and judges; freeze the protocol, endpoints, model versions, sample size, and analysis plan. |
| Oct 1-14 | Generate the full response set; complete human annotation and calibrated automated evaluation. |
| Oct 15-21 | Conduct primary analysis, robustness checks, mitigation, and qualitative error analysis. |
| Oct 22-Nov 3 | Write the paper and prepare the benchmark, code, documentation, data statement, and reproducibility package. |

### 5. Expected contributions and success criteria

The intended contributions are: (1) a controlled, versioned age-counterfactual medical benchmark; (2) a clinician-validated rubric separating beneficial adaptation from inappropriate treatment; (3) reproducible evidence about model and scenario factors associated with unsafe age conditioning; and (4) a tested mitigation with an explicit benefit-harm tradeoff.

The study will proceed to submission only if prompt pairs preserve identical clinical facts, all records are joined by stable IDs, no invalid evaluator output is silently replaced, clinician review is completed, automated evaluators meet a prespecified reliability threshold, and all reported results can be regenerated from a clean environment. FAccT 2027 is a possible primary target, subject to an October 20 quality review; CHIL or MLHC 2027 would be preferable if clinical validation is incomplete.

### 6. Decisions requested from the advisor

1. Is the revised framing—appropriate versus inappropriate age adaptation—the right central contribution?
2. May the previous results be treated as pilot evidence while the core experiment is rebuilt?
3. Can we secure two clinical raters and an adjudicator, including compensation if needed?
4. What API/GPU budget, data-governance review, and IRB determination are required?
5. Which submission venue and authorship responsibilities should guide the eight-week plan?
