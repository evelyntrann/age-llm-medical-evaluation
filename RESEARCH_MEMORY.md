# Research Project Memory

**Last updated:** September 2, 2026  
**Purpose:** durable context for continuing the project across sessions. This is a decision-and-evidence log, not a transcript. Do not store API keys, credentials, protected health information, or unpublished reviewer identities here.

## Researcher's goal

Take over the inherited age/LLM/medical-evaluation project, understand why the MLHC 2026 submission failed, rebuild it into a clinically defensible and reproducible study, and prepare a comprehensive paper. The researcher can work intensively for two months. September 30 is the protocol/pilot milestone; November 3 is the realistic end of the eight-week execution window.

## Current strategic decision

- Preserve the inherited work as a pilot, but do not extend its datasets or reuse its reported numbers without reconstruction.
- Reframe the paper around **clinically appropriate versus inappropriate age-conditioned adaptation**, not “any deviation from an age-neutral answer equals bias.”
- Working title: **When Should Age Matter? Clinically Calibrated Counterfactual Auditing of Age-Conditioned Health Advice in Large Language Models**.
- Clinical validity, pairing integrity, judge validation, uncertainty, and reproducibility are core. Tone metrics and embeddings are secondary or future work.
- Conditional primary target: FAccT 2027 (abstract October 27, paper November 3). Do not submit on schedule alone; use an October 20 quality gate. CHIL/MLHC 2027 is the fallback when calls are available.

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
- Create neutral plus exact-age variants by deterministic insertion only; never use an LLM to rewrite clinical facts.
- Evaluate four complementary model families with frozen identifiers, prompts, and settings.
- Primary label: inappropriate age-conditioned clinical change. Separate appropriate adaptation, equivalence, unsupported stereotypes, under/over-triage, unsafe action, omitted escalation, and unsupported certainty.
- Obtain two-clinician blinded ratings with adjudication for at least 400 stratified paired comparisons; use pilot estimates to finalize sample size.
- Calibrate two LLM-judge families against the human set and test direct evaluator age sensitivity.
- Analyze paired absolute risk differences with cluster-bootstrap confidence intervals and mixed-effects models.
- Test one prespecified prompt mitigation without sacrificing beneficial adaptation.

The advisor-facing version is in `ADVISOR_RESEARCH_PLAN.md`.

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

## Memory maintenance protocol

At the start of each substantive session, read this file and the two linked planning documents. Before ending, update the date, decisions, exact files changed, tests or analyses run, results, blockers, and the next concrete action. Preserve earlier entries; correct errors explicitly rather than silently rewriting history.
