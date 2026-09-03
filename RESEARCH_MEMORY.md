# Research Project Memory

**Last updated:** September 2, 2026  
**Purpose:** durable context for continuing the project across sessions. This is a decision-and-evidence log, not a transcript. Do not store API keys, credentials, protected health information, or unpublished reviewer identities here.

## Researcher's goal

Take over the inherited age/LLM/medical-evaluation project, understand why the MLHC 2026 submission failed, rebuild it into a clinically defensible and reproducible study, and prepare a comprehensive paper. The researcher can work intensively for two months. September 30 is the protocol/pilot milestone; November 3 is the realistic end of the eight-week execution window.

## Current strategic decision

- Preserve the inherited work as a pilot, but do not extend its datasets or reuse its reported numbers without reconstruction.
- Reframe the paper around **clinically appropriate versus inappropriate age-conditioned adaptation**, not “any deviation from an age-neutral answer equals bias.”
- Use a two-sided primary framework: over-conditioning when age should not matter and under-conditioning when age should matter; report harmful and appropriate adaptation separately.
- Working title: **When Should Age Matter? Clinically Calibrated Counterfactual Auditing of Age-Conditioned Health Advice in Large Language Models**.
- Clinical validity, pairing integrity, judge validation, uncertainty, and reproducibility are core. Tone metrics and embeddings are secondary or future work.
- Venue decision revised after literature review: CHIL/MLHC is the natural fit for a clinically centered benchmark. FAccT 2027 is conditional on meaningful older-adult/patient or health-equity stakeholder engagement and deeper sociotechnical analysis. Do not submit on schedule alone.

## Confirmed repository state

- Audited commit: `a434a13c` on `master`; four commits were present at audit time.
- The repository has six notebooks, two metric modules, two prompt CSVs, the thesis PDF, plots/text outputs, and a large pinned requirements file.
- It lacks tests, CI, a release/tag, a data manifest, and the complete raw response/audit artifacts necessary for reproduction.
- `base_prompts.csv`: 3,160 rows and 3,152 unique questions.
- `gen_prompts.csv`: 53,585 rows and 10,717 rows per age label, conflicting with the paper's 53,395/10,679 counts.
- Generated scenario alignment is corrupted beginning at zero-based group 4,055, and many “counterfactuals” change clinical content in addition to age.
- GPT Batch outputs are assigned by return order rather than keyed `custom_id`; downstream shifts are possible.
- The MedGemma judge does not receive the clinical question; invalid outputs are common and asymmetric defaults bias ADSB.
- Saved result files and notebook outputs contain incompatible sample sizes, sign conventions, and at least one impossible aggregate value.
- The embedding notebook's pooling differs from the paper, expected input is missing, and its outputs are internally inconsistent.

Full evidence and remediation requirements are in `REPRODUCTION_AUDIT.md`.

## Reviewer feedback to keep central

- The age manipulation changes more than age.
- The study does not distinguish beneficial clinical adaptation from age bias.
- The single automated judge lacks clinical validation and could have its own age sensitivity.
- Metrics and severity weights need clinical justification.
- Model coverage is weak, especially the tiny Llama comparator.
- Mechanistic and mitigation contributions are missing or overstated.
- A clinical reviewer still found the topic relevant, novel, and potentially useful if validation and reproducibility improve.

## Approved working design pending advisor feedback

- Curate 800-1,000 licensed, first-person scenarios; stratify as age-invariant, age-relevant, or age-conditional and by acuity/domain.
- Prioritize a clinician-validated gold core over reaching the maximum scenario count; add an extended set only after core quality gates pass.
- Create neutral plus exact-age variants by deterministic insertion only; never use an LLM to rewrite clinical facts.
- Evaluate four complementary model families with frozen identifiers, prompts, and settings.
- Primary label: inappropriate age-conditioned clinical change. Separate appropriate adaptation, equivalence, unsupported stereotypes, under/over-triage, unsafe action, omitted escalation, and unsupported certainty.
- Obtain two-clinician blinded ratings with adjudication for at least 400 stratified paired comparisons; use pilot estimates to finalize sample size.
- Calibrate two LLM-judge families against the human set and test direct evaluator age sensitivity.
- Analyze paired absolute risk differences with cluster-bootstrap confidence intervals and mixed-effects models.
- Test one prespecified prompt mitigation without sacrificing beneficial adaptation.

The current advisor-facing version is `ADVISOR_FIRST_MEETING_PROPOSAL_V2.md`; the earlier proposal is retained but marked superseded. The evidence basis and conference-style critique are in `EVIDENCE_REVIEW_AND_PROPOSAL_REASSESSMENT.md`.

## Immediate next actions

1. Send the two-page plan and audit summary to the advisor.
2. Ask for clinician access, annotation/API/GPU budget, data-governance or IRB determination, target venue, and authorship roles.
3. Inventory any unpublished raw batch outputs, audit CSVs, model/version records, and prior code from the former team.
4. Create the new immutable scenario schema and 100-case benchmark; do not edit or delete legacy artifacts.
5. Draft the clinician rubric and pilot protocol before generating the full dataset.

## Open decisions

- Exact models and snapshots, selected after cost/access checks and frozen before the pilot.
- Source datasets and their redistribution licenses.
- Clinician availability and compensated annotation hours.
- Prespecified evaluator-agreement threshold and sample-size calculation after pilot prevalence.
- Whether institutional review or exemption documentation is required.

## Session log

### 2026-09-02 — Repository and review audit

- Read the repository structure, README, six notebooks, metric code, committed datasets/results, thesis, supplied MLHC reviews, and prior conversation.
- Verified fundamental data-lineage, evaluator, metric, and reproducibility failures; concluded that a clean rebuild is required.
- Established the revised clinical framing and eight-week staged plan.
- Added `ADVISOR_RESEARCH_PLAN.md`, `REPRODUCTION_AUDIT.md`, and this memory file.
- Next session should begin with advisor feedback or, if not yet available, the 100-case benchmark schema and annotation rubric.

### 2026-09-02 — First advisor meeting proposal

- Added `ADVISOR_FIRST_MEETING_PROPOSAL.md`, a concise two-page version intended for the first detailed advisor discussion.
- Kept the audit summary diplomatic and centered the document on the revised contribution, controlled benchmark, clinician validation, paired analysis, eight-week milestones, quality gates, and decisions needed from the advisor.
- No research-design decision changed; advisor approval and access to clinical raters remain the immediate blockers.
- Next action: personalize the researcher/advisor fields, send the proposal before the meeting if appropriate, and record the advisor's decisions afterward.

### 2026-09-02 — Staff-level strengthening and technical architecture

- Compared the rebuilt design with the inherited study and documented the comparison in `PLAN_STRENGTHENING_AND_TECH_STACK.md`.
- Strengthened both advisor plans with co-primary over-conditioning and under-conditioning outcomes, clinician-defined expected response dimensions, and separate absolute-answer and paired-difference ratings.
- Recommended a tiered dataset: clinician-validated gold core first, optional scale extension second.
- Identified a 100-scenario clinical-mediator factorial set as the highest-value stretch goal, conditional on completing the core study.
- Chose regular Python as the source of truth; Colab is optional compute for pilots, notebooks are thin analysis interfaces, and C++ is not needed.
- Recommended Python 3.11, `uv`, a `src/` package, Parquet/JSONL, strict schemas, provider SDKs, Transformers/vLLM, Label Studio or institution-approved REDCap, tested statistics, manifests, CI, and an eventual minimal container.
- Next action: obtain advisor feedback on the two-sided endpoints, clinician availability, gold-core size, stretch experiment, and compute/annotation resources before restructuring the repository.

### 2026-09-02 — Clarified external dependencies and clinical workflow

- Clarified that the researcher prepares and quality-checks the candidate questions, deterministic age variants, model responses, identifiers, and annotation package.
- Clinical involvement has two checkpoints: early validation of the 100-case pilot/rubric and later independent rating of a stratified answer-pair subset.
- The two clinicians do not need to review all 800-1,000 questions or all model outputs; the proposed minimum remains 400 paired comparisons for the gold evaluation set, with the final size determined from the pilot.
- Updated `ADVISOR_FIRST_MEETING_PROPOSAL.md` to make this division of work explicit.
- Major external dependencies remain clinician access, advisor approval, data-governance/IRB guidance, and compute/annotation budget.

### 2026-09-02 — Evidence review and conference-standard reassessment

- Conducted a targeted narrative review of peer-reviewed medical-LLM evaluation, health-equity, counterfactual fairness, LLM-judge, rubric, ageism, and reporting research, plus official FAccT, CHIL, and MLHC criteria.
- Concluded that the earlier revised proposal fixes the inherited study but remains vulnerable on novelty, rater design, age-stratum justification, rare-event power, evaluator validation, and FAccT sociotechnical fit.
- Created `EVIDENCE_REVIEW_AND_PROPOSAL_REASSESSMENT.md` with the evidence-to-design mapping and a conference-style assessment.
- Created `ADVISOR_FIRST_MEETING_PROPOSAL_V2.md` and marked the earlier proposal superseded.
- Revised the intended benchmark to separate a representative naturalistic set from an enriched clinician challenge set; their rates must not be pooled.
- Upgraded the rater target from two clinicians to a panel of three to four, with at least two independent ratings per gold item, partial triple-rating, adjudication, training, and domain matching.
- Added clinically justified adult age anchors, separate handling of pediatric cases, repeated-generation reliability checks, criterion-level judge validation, and pilot/simulation-based power around a minimum clinically important difference.
- Reframed novelty as calibrated reliance on age and retained the clinical-mediator factorial design as the main stretch contribution.
- Reclassified FAccT as conditional on meaningful stakeholder and sociotechnical engagement; otherwise prefer CHIL/MLHC when their 2027 calls are available.
- Recorded that FAccT 2027's current policy requires AI-use disclosure and prohibits LLM-generated publication prose; planning material must not be copied into the eventual manuscript as authorial text.
- Next action: discuss V2 with the advisor and obtain decisions on target use case, adult/pediatric scope, clinician panel, stakeholder involvement, minimum clinically important effect, venue, IRB, and budget before building the pilot.

## Memory maintenance protocol

At the start of each substantive session, read this file and the two linked planning documents. Before ending, update the date, decisions, exact files changed, tests or analyses run, results, blockers, and the next concrete action. Preserve earlier entries; correct errors explicitly rather than silently rewriting history.
