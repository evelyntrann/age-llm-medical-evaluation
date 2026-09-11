"""
Workstream A -- Scenario Pool Refinement (Phase2_Methodology_Plan.pdf, Section 2A).

Narrows data/base_prompts.csv (10,717 deduplicated counsel_chat + healthsearchqa
questions) into a smaller, well-characterized pool sized for hand annotation:

  1. Semantic (not just exact-string) de-duplication.
  2. Coarse clinical topic/category tag per scenario.
  3. Flag scenarios that are already inherently age-anchored in their base text
     (can't be neutrally recombined across all four age groups).
  4. Stratified sample down to a target curated-pool size (default 200, plan
     range is 150-300).
  5. Write data/scenario_pool_v2.csv -- the curated pool itself (id, question,
     category), matching what the plan describes annotators will open --
     plus the full annotated pool (all scenarios, with dedup/age-anchor/
     selection columns) as an audit trail under
     evelyn/workstream_a_scenario_pool/full_annotated_pool.csv, and a
     selection log. The original data/base_prompts.csv is never modified.

Similarity backend: TF-IDF + cosine similarity, implemented with only numpy/pandas
(both already in requirements.txt). This environment doesn't have torch/
sentence-transformers installed, and pulling in a transformer embedding model just
for this pass wasn't worth the dependency weight -- TF-IDF still catches
near-duplicate phrasings that exact-string matching misses, which is the gap the
plan calls out. If tighter semantic recall is needed later, swap `_tfidf_vectors`
for embeddings from an already-available model (e.g. the Llama checkpoint used in
notebook 05) and keep the union-find clustering step as-is.

Usage:
    python evelyn/workstream_a_scenario_pool/refine_scenario_pool.py
    python evelyn/workstream_a_scenario_pool/refine_scenario_pool.py --pool-size 250
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
# NOTE: the plan (Phase2_Methodology_Plan.pdf, Section 2A) cites data/base_prompts.csv
# as "the existing 10,679 base scenarios," but that file only has 3,160 rows in this
# repo (verified against git history -- not a local edit, it's been that size since
# the initial commit). The row count that actually matches (10,717) lives in
# data/gen_prompts.csv under age_group == "base_prompt" -- almost certainly what the
# plan meant to point at. Sourcing from there instead; see selection_log.md for the
# full note.
GEN_PROMPTS_PATH = REPO_ROOT / "data" / "gen_prompts.csv"
CURATED_POOL_CSV_PATH = REPO_ROOT / "data" / "scenario_pool_v2.csv"
FULL_AUDIT_CSV_PATH = Path(__file__).resolve().parent / "full_annotated_pool.csv"
SELECTION_LOG_PATH = Path(__file__).resolve().parent / "selection_log.md"

DEFAULT_POOL_SIZE = 200
DUPLICATE_SIMILARITY_THRESHOLD = 0.90
RANDOM_SEED = 42
SIMILARITY_CHUNK_SIZE = 1000

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "of", "at", "by", "for", "with",
    "about", "against", "between", "into", "through", "during", "before", "after",
    "to", "from", "in", "on", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "should", "can",
    "could", "i", "you", "he", "she", "it", "we", "they", "my", "your", "his",
    "her", "its", "our", "their", "this", "that", "these", "those", "what",
    "which", "who", "whom", "as", "so", "than", "too", "very", "just", "not",
    "no", "there", "here", "how", "why", "when", "where", "me", "им",
}

# Coarse clinical topic taxonomy. Keyword lists are a first-pass heuristic --
# meant to make later stratified sampling non-ad-hoc, not a clinically validated
# labeling. Flag for review once a clinical collaborator is on the team (per the
# plan's Section 4 handoff packet).
CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "mental_health": [
        "anxiety", "anxious", "depress", "therapy", "therapist", "counsel",
        "stress", "grief", "trauma", "mood", "suicid", "self-harm", "self harm",
        "panic attack", "ptsd", "bipolar", "ocd", "addiction", "substance abuse",
        "alcoholism", "eating disorder", "loneliness", "insomnia", "psychiat",
    ],
    "cardiovascular": [
        "heart", "cardiac", "blood pressure", "hypertension", "cholesterol",
        "chest pain", "stroke", "artery", "arrhythmia", "palpitation",
    ],
    "respiratory": [
        "lung", "asthma", "breath", "cough", "pneumonia", "copd", "bronchitis",
        "wheez", "sinus",
    ],
    "neurological": [
        "brain", "headache", "migraine", "seizure", "epilep", "nerve",
        "dizziness", "memory loss", "numbness", "concussion", "tremor",
    ],
    "gastrointestinal": [
        "stomach", "digest", "nausea", "vomit", "diarrhea", "constipation",
        "liver", "ibs", "bowel", "acid reflux", "heartburn", "gallbladder",
    ],
    "musculoskeletal": [
        "bone", "joint", "muscle", "back pain", "arthritis", "fracture",
        "sprain", "tendon", "ligament", "osteoporosis",
    ],
    "dermatology": [
        "skin", "rash", "acne", "eczema", "mole", "itch", "psoriasis", "hives",
    ],
    "reproductive_sexual_health": [
        "pregnan", "menstrua", "period cramps", "sexual", "std", "sti",
        "fertility", "contracept", "menopause", "prostate", "erectile",
        "birth control",
    ],
    "oncology": [
        "cancer", "tumor", "tumour", "chemo", "biopsy", "malignant", "leukemia",
        "carcinoma",
    ],
    "endocrine_metabolic": [
        "diabet", "thyroid", "hormone", "metabolism", "insulin", "obesity",
        "weight gain", "weight loss",
    ],
    "infectious_disease": [
        "infection", "virus", "bacteria", "flu", "influenza", "fever",
        "contagious", "covid", "measles", "std", "hepatitis",
    ],
    "injury_first_aid": [
        "burn", "wound", "bleeding", "accident", "emergency", "choking",
        "poison", "concussion", "cpr", "first aid",
    ],
    "medication_pharmacology": [
        "medication", "medicine", "drug interaction", "dosage", "side effect",
        "prescription", "pill", "overdose", "antibiotic",
    ],
    "nutrition_lifestyle": [
        "diet", "exercise", "nutrition", "vitamin", "sleep", "hydration",
        "supplement", "lifestyle",
    ],
}
CATEGORY_PRIORITY = list(CATEGORY_KEYWORDS.keys())
FALLBACK_CATEGORY = "other_general"

# Terms that anchor a scenario to a specific life stage in its *base* text, making
# it unsafe to neutrally recombine across all four age-conditioning groups
# (teen / young_adult / middle_aged / senior).
AGE_ANCHOR_KEYWORDS = [
    "infant", "newborn", "toddler", "baby", "babies", "pediatric", "school-age",
    "teenager", "adolescen", "puberty", "my son", "my daughter", "my child",
    "my kid", "my toddler", "my baby", "menopause", "elderly", "geriatric",
    "senior citizen", "nursing home", "retirement", "breastfeeding",
    # Bare "child(ren)" catches direct pediatric framing ("skin rash in
    # children") that "my child" alone misses. Trade-off: it will also flag a
    # question that merely mentions a child in passing (e.g. a custody
    # dispute), which isn't really age-anchored -- but over-flagging into the
    # set-aside pile (not deleted, just excluded from this pool) is the safer
    # failure mode than a genuinely pediatric-only scenario slipping into the
    # "recombine across all four age groups" pool.
    "child", "children", "kid", "kids",
]

# Numeric self-reported ages ("I'm 47 and...", "17-year-old", "17 y/o", "29M",
# "22F") anchor a scenario just as much as a life-stage word does, but none of
# the keywords above catch them. Checked directly against this corpus: 56% of
# the 10,717 base scenarios state an explicit numeric age this way, and the
# keyword list alone caught only 232 of those 6,006 (3.9%) -- most "base"
# scenarios that look age-neutral by category actually already have a specific
# age baked in. The forum-shorthand pattern ("27M", "22F,") adds a further 31
# scenarios the "I'm N" phrasing alone misses; spot-checked with no false
# positives against height-in-meters mentions in this corpus.
# A manual read-through of the 200-scenario curated pool (regex/keyword
# matching alone keeps missing new phrasings -- natural language has too many
# ways to state an age to enumerate exhaustively) turned up three more
# patterns: a leading forum-post age+spelled-out-sex ("28, Male, 6'1\"..."), a
# spelled-out decade band ("in my early 30s", "in his late thirties"), and a
# past-age reference ("since I was 19") that still anchors the narrative even
# though it's a lower bound, not a current age.
AGE_ANCHOR_NUMERIC_PATTERN = re.compile(
    r"\b(?:i'?m|i am|aged?)\s+\d{1,3}\b"
    r"|\b\d{1,3}[- ]years?[- ]old\b"
    r"|\b\d{1,3}\s*y/?o\b"
    r"|\b\d{1,3}\s*[mf]\b[,.\s]"
    r"|\b\d{1,3},?\s*(?:male|female)\b"
    r"|\bin (?:my|his|her|their) (?:early|mid|late)?\s*"
    r"(?:twenties|thirties|forties|fifties|sixties|seventies|eighties|20s|30s|40s|50s|60s|70s)\b"
    r"|\b(?:since|when) i (?:was|turned) \d{1,3}\b"
    # Reversed forum shorthand ("M 47" instead of "47M"). The lookbehind
    # excludes a preceding letter/apostrophe specifically to stop this from
    # matching the "m" in a contraction like "I'm 17" -- an earlier, looser
    # version of this pattern matched 5,982 rows for exactly that reason
    # before the lookbehind was added; tightened version matches 3 genuine
    # hits with no false positives found.
    r"|(?<![a-z'])[mf]\s+\d{1,3}\b"
    r"|\b(?:male|female)\s*,?\s*\d{1,3}\b",
    re.IGNORECASE,
)

# Found by manually reading the curated pool (id, reason). These aren't caught
# by any generalizable pattern -- one is a structural mismatch with the
# age-conditioning premise, the other needs advisor/clinical sensitivity
# review regardless of age-anchoring mechanics. IDs are stable as long as
# data/gen_prompts.csv doesn't change (id = row order of age_group ==
# "base_prompt"), since _load_base_scenarios assigns them by that order.
MANUAL_AGE_ANCHOR_EXCLUSIONS: dict[int, str] = {
    3565: "third-person caregiving question (a day-camp counselor asking how "
    "to manage a child's behavior) -- the age-conditioning premise assumes "
    "the asker/patient's own age varies, which doesn't apply when the "
    "question is about advising on someone else's care",
    3585: "involves a specific near-age-10 minor (\"he isn't quite 10\") and "
    "content (\"is this a deviant act\") that needs advisor/clinical "
    "sensitivity review before use in any annotation exercise, independent "
    "of the age-anchoring question",
    3952: "\"after 40 years of being straight\" implies a much older adult "
    "(at least ~50s) with no matching numeric-age pattern -- can't be "
    "neutrally recombined into a teen or young_adult framing",
    3809: "\"my new daughter-in-law\" plus \"I just lost my mom\" implies a "
    "parent of a married adult child, i.e. at least middle-aged -- rules out "
    "teen/young_adult, no matching numeric-age pattern",
    3496: "\"my school is small,\" \"track meet,\" \"my dad wants me to\" -- "
    "strong implicit school-age/teen context (competitive youth sports under "
    "parental authority) too idiomatic to generalize into a safe regex "
    "without risking false positives on unrelated \"school\" mentions",
}

# Found the same way: a keyword-based category tag can mis-fire on an
# incidental word match. "child custody concerns, financial issues... weight
# gain" tagged endocrine_metabolic purely off "weight gain," but the scenario
# is a mental-health coping narrative.
MANUAL_CATEGORY_OVERRIDES: dict[int, str] = {
    3905: "mental_health",
}


def _normalize(text: str) -> str:
    # Many scraped questions use a typographic right single quote (’) for
    # contractions ("I’m 16") instead of a straight apostrophe. Left
    # unnormalized, "i’m" doesn't match "i'm" in either the tokenizer's
    # character class or the age-anchor regex below, silently missing a real
    # chunk of self-reported ages (confirmed on this corpus).
    return text.lower().replace("’", "'")


def _tokenize(text: str) -> list[str]:
    # Keep digits, not just letters: numbers ("3 types" vs "4 types", a fever of
    # 106 vs 103) are often the clinically distinguishing content in an
    # otherwise identical question template, so dropping them causes false
    # near-duplicate matches (confirmed on this corpus).
    words = re.findall(r"[a-z0-9']+", _normalize(text))
    # len(w) > 1 drops stray single letters, but a bare single-digit count
    # ("3 types" vs "4 types") is exactly the kind of short, meaningful token
    # this dedup step needs to keep -- isdigit() carves out that exception.
    return [w for w in words if w not in STOPWORDS and (len(w) > 1 or w.isdigit())]


def _tfidf_vectors(documents: list[str]) -> np.ndarray:
    """Dependency-free TF-IDF over the full corpus vocabulary.

    Deliberately does NOT cap the vocab to the most-frequent terms: for
    near-duplicate detection the rare, high-IDF terms (specific diagnoses like
    "preeclampsia" or "spina bifida") are exactly the ones that distinguish two
    otherwise-similar-looking questions, while the frequent terms ("baby",
    "survive", "person") are the generic template words shared by many
    unrelated questions. Dropping rare terms to bound vocab size collapses
    distinct scenarios onto identical vectors -- confirmed on this corpus (a
    4,000-term cap produced cosine similarity of exactly 1.0 between "Can a
    baby survive preeclampsia?" and "Can a baby survive after stillbirth?").
    The full vocabulary here is under 10k terms, so there's no memory reason to
    truncate it anyway.
    """
    tokenized = [_tokenize(doc) for doc in documents]

    doc_freq: Counter[str] = Counter()
    for tokens in tokenized:
        doc_freq.update(set(tokens))

    vocab = list(doc_freq.keys())
    vocab_index = {term: i for i, term in enumerate(vocab)}
    n_docs = len(documents)

    idf = np.zeros(len(vocab), dtype=np.float32)
    for term, i in vocab_index.items():
        idf[i] = np.log((1 + n_docs) / (1 + doc_freq[term])) + 1.0

    matrix = np.zeros((n_docs, len(vocab)), dtype=np.float32)
    for row, tokens in enumerate(tokenized):
        counts = Counter(t for t in tokens if t in vocab_index)
        if not counts:
            continue
        total = sum(counts.values())
        for term, count in counts.items():
            col = vocab_index[term]
            matrix[row, col] = (count / total) * idf[col]

    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return matrix / norms


def _cluster_near_duplicates(vectors: np.ndarray, threshold: float) -> np.ndarray:
    """Union-find over cosine similarity, processed in row chunks to bound peak
    memory. Returns an array mapping each row index to its cluster's lowest
    original index (the cluster representative)."""
    n = vectors.shape[0]
    parent = np.arange(n)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    for start in range(0, n, SIMILARITY_CHUNK_SIZE):
        end = min(start + SIMILARITY_CHUNK_SIZE, n)
        # Compare this chunk against itself and every later row (i < j only).
        sims_to_rest = vectors[start:end] @ vectors[start:].T
        rows, cols = np.where(sims_to_rest > threshold)
        for r, c in zip(rows, cols):
            i, j = start + r, start + c
            if i < j:
                union(i, j)

    return np.array([find(i) for i in range(n)])


def _assign_category(question: str) -> str:
    lower = _normalize(question)
    scores = {
        category: sum(1 for kw in keywords if kw in lower)
        for category, keywords in CATEGORY_KEYWORDS.items()
    }
    best_category = max(CATEGORY_PRIORITY, key=lambda c: scores[c])
    return best_category if scores[best_category] > 0 else FALLBACK_CATEGORY


def _find_age_anchor(question: str) -> str | None:
    lower = _normalize(question)
    for keyword in AGE_ANCHOR_KEYWORDS:
        if keyword in lower:
            return keyword
    match = AGE_ANCHOR_NUMERIC_PATTERN.search(lower)
    return match.group(0) if match else None


def _stratified_sample(eligible: pd.DataFrame, pool_size: int, seed: int) -> set[int]:
    rng = np.random.default_rng(seed)
    category_counts = eligible["category"].value_counts()
    total_eligible = len(eligible)
    selected_ids: set[int] = set()

    quotas = {
        category: max(1, round(pool_size * count / total_eligible))
        for category, count in category_counts.items()
    }

    for category, quota in quotas.items():
        candidates = eligible.loc[eligible["category"] == category, "id"].to_numpy()
        take = min(quota, len(candidates), pool_size - len(selected_ids))
        if take <= 0:
            continue
        chosen = rng.choice(candidates, size=take, replace=False)
        selected_ids.update(chosen.tolist())

    # Quota rounding can under/overshoot; top up from remaining eligible rows.
    if len(selected_ids) < pool_size:
        remaining = eligible.loc[~eligible["id"].isin(selected_ids), "id"].to_numpy()
        shortfall = pool_size - len(selected_ids)
        if len(remaining) > 0:
            top_up = rng.choice(remaining, size=min(shortfall, len(remaining)), replace=False)
            selected_ids.update(top_up.tolist())

    return selected_ids


def _load_base_scenarios() -> pd.DataFrame:
    gen = pd.read_csv(GEN_PROMPTS_PATH)
    base_rows = gen.loc[gen["age_group"] == "base_prompt", ["prompt"]].reset_index(drop=True)
    base_rows = base_rows.rename(columns={"prompt": "question"})
    base_rows.insert(0, "id", base_rows.index + 1)
    return base_rows


def refine_scenario_pool(pool_size: int = DEFAULT_POOL_SIZE, seed: int = RANDOM_SEED) -> pd.DataFrame:
    base = _load_base_scenarios()
    questions = base["question"].tolist()

    vectors = _tfidf_vectors(questions)
    cluster_reps = _cluster_near_duplicates(vectors, DUPLICATE_SIMILARITY_THRESHOLD)

    base_ids = base["id"].to_numpy()
    is_duplicate = cluster_reps != np.arange(len(base))
    duplicate_of_id = np.where(is_duplicate, base_ids[cluster_reps], -1)

    base["category"] = base["question"].map(_assign_category)
    for scenario_id, corrected_category in MANUAL_CATEGORY_OVERRIDES.items():
        base.loc[base["id"] == scenario_id, "category"] = corrected_category

    age_anchor = base["question"].map(_find_age_anchor)
    base["age_anchored"] = age_anchor.notna()
    base["age_anchor_keyword"] = age_anchor.fillna("")
    for scenario_id, reason in MANUAL_AGE_ANCHOR_EXCLUSIONS.items():
        base.loc[base["id"] == scenario_id, "age_anchored"] = True
        base.loc[base["id"] == scenario_id, "age_anchor_keyword"] = f"[manual] {reason}"

    base["is_duplicate"] = is_duplicate
    base["duplicate_of_id"] = duplicate_of_id

    eligible = base[~base["is_duplicate"] & ~base["age_anchored"]]
    selected_ids = _stratified_sample(eligible, pool_size, seed)
    base["selected_for_curated_pool"] = base["id"].isin(selected_ids)

    audit_columns = [
        "id", "question", "category", "is_duplicate", "duplicate_of_id",
        "age_anchored", "age_anchor_keyword", "selected_for_curated_pool",
    ]
    full_audit = base[audit_columns]
    full_audit.to_csv(FULL_AUDIT_CSV_PATH, index=False)

    curated_pool = base.loc[base["selected_for_curated_pool"], ["id", "question", "category"]]
    curated_pool.to_csv(CURATED_POOL_CSV_PATH, index=False)

    _write_selection_log(base, eligible, selected_ids, pool_size)
    return curated_pool


def _write_selection_log(
    base: pd.DataFrame, eligible: pd.DataFrame, selected_ids: set[int], pool_size: int
) -> None:
    total = len(base)
    n_duplicates = int(base["is_duplicate"].sum())
    n_age_anchored = int(base["age_anchored"].sum())
    n_eligible = len(eligible)
    n_selected = len(selected_ids)

    category_table = (
        base.groupby("category")
        .agg(
            total=("id", "count"),
            duplicates=("is_duplicate", "sum"),
            age_anchored=("age_anchored", "sum"),
            selected=("selected_for_curated_pool", "sum"),
        )
        .sort_values("total", ascending=False)
    )

    lines = [
        "# Workstream A -- Scenario Pool Selection Log",
        "",
        f"Source: `data/gen_prompts.csv` rows where `age_group == \"base_prompt\"` "
        f"({total} scenarios). `data/base_prompts.csv` is left untouched, as the "
        "plan requires for the original submitted set.",
        "Output: `data/scenario_pool_v2.csv` (the curated pool itself -- id, "
        "question, category -- for hand annotation) plus "
        "`evelyn/workstream_a_scenario_pool/full_annotated_pool.csv` (every "
        "scenario with its dedup/age-anchor/selection flags, kept as the audit "
        "trail for what was dropped and why).",
        "",
        "**Source-file note:** the plan (Section 2A) cites `data/base_prompts.csv` "
        "as \"the existing 10,679 base scenarios,\" but that file has only 3,160 "
        "rows in this repo (confirmed via git history, not a local edit -- it's "
        "been that size since the initial commit). The row count that actually "
        "matches (10,717) lives in `data/gen_prompts.csv` under "
        "`age_group == \"base_prompt\"`, so this run sources from there instead. "
        "Worth confirming with the advisor which file was actually meant, and "
        "why `base_prompts.csv` is so much smaller than the generation output it "
        "should be a snapshot of.",
        "",
        "## Pipeline summary",
        "",
        f"- Starting pool: **{total}** scenarios.",
        f"- Near-duplicates removed (TF-IDF cosine similarity > "
        f"{DUPLICATE_SIMILARITY_THRESHOLD}): **{n_duplicates}** "
        f"({n_duplicates / total:.1%}).",
        f"- Flagged as age-anchored in base text (set aside, not deleted): "
        f"**{n_age_anchored}** ({n_age_anchored / total:.1%}).",
        f"- Eligible for the curated pool (not a duplicate, not age-anchored): "
        f"**{n_eligible}**.",
        f"- Curated pool target size: **{pool_size}**; actually selected: "
        f"**{n_selected}**.",
        "",
        "## Category breakdown",
        "",
        "| Category | Total | Duplicates | Age-anchored | Selected |",
        "|---|---|---|---|---|",
    ]
    for category, row in category_table.iterrows():
        lines.append(
            f"| {category} | {row['total']} | {row['duplicates']} | "
            f"{row['age_anchored']} | {row['selected']} |"
        )

    lines += [
        "",
        "## Manual review pass",
        "",
        "Regex/keyword matching alone kept missing new age-anchor phrasings on "
        "every pass, because natural language has too many ways to state an "
        "age to enumerate exhaustively. Four rounds of manually reading the "
        "curated 200-scenario pool (not the full 10,717 -- too large to read "
        "by hand), each after regenerating the sample, found real leaks each "
        "time: bare \"child(ren)\"/\"kid(s)\", spelled-out decade bands (\"in my "
        "early 30s\"), past-age references (\"since I was 19\"), forum "
        "shorthand in both orders (\"29M\", \"M 47\", \"Male, 26\"), and a "
        "handful of one-off cases folded into `MANUAL_AGE_ANCHOR_EXCLUSIONS` / "
        "`MANUAL_CATEGORY_OVERRIDES` (a structural mismatch with the "
        "age-conditioning premise, content needing advisor sensitivity "
        "review, a keyword-driven category mis-tag, and implicit family-role "
        "anchors too idiomatic to generalize into regex, like \"my school is "
        "small\" or \"my daughter-in-law\").",
        "",
        "**This converges but doesn't guarantee completeness.** Softer "
        "implicit signals were deliberately left unflagged rather than chased "
        "indefinitely -- e.g. a scenario mentioning \"my wife and daughter\" "
        "rules out a teen framing but not young_adult/middle_aged/senior, so "
        "it's a weaker anchor than an explicit number and a judgment call "
        "rather than a clear violation. Workstream B's own annotation process "
        "is the right place to catch these residual cases: if a reviewer "
        "notices a scenario implies a specific life stage through family role "
        "or context without a hard numeric anchor, that belongs in the "
        "`rationale` field (and `needs_clinical_review` if it affects the "
        "label), not a silent guess. **If the pool is regenerated with a "
        "materially different sample, repeat this manual read-through** -- "
        "these fixes target the specific scenarios found across four rounds, "
        "not the full pattern space.",
        "",
        "## Methodology notes / known limitations",
        "",
        "- **Dedup backend is TF-IDF + cosine similarity**, not neural sentence "
        "embeddings -- this environment has no torch/sentence-transformers "
        "installed. It catches near-identical phrasings (shared vocabulary) but "
        "will miss paraphrases that reword a question with different words for "
        "the same underlying complaint. Upgrading to embeddings from an "
        "already-available checkpoint (e.g. the Llama model used in notebook 05) "
        "is a drop-in replacement for `_tfidf_vectors` if recall needs to be "
        "tighter.",
        "- **Manual spot-check of ~30 flagged duplicate pairs found one residual "
        "false-positive pattern**: two short questions on the same topic but "
        "different intent (e.g. \"What is X surgery?\" vs \"Is X surgery "
        "painful?\") can still clear the 0.90 threshold when the shared topic "
        "words dominate a very short bag-of-words vector. Two sharper bugs in "
        "this category were already caught and fixed while building this script "
        "(vocab truncation collapsing distinct diagnoses to identical vectors; "
        "digit tokens being stripped so \"3 types\" and \"4 types\" matched) -- "
        "if a full re-audit of the duplicate list turns up more of the "
        "surviving pattern, the fix is a stricter threshold (try 0.95) traded "
        "against catching fewer true paraphrases, not another representation "
        "change.",
        "- **Category tags are keyword-based**, not clinically validated. They "
        "exist so stratified sampling isn't ad hoc (plan Section 2A, item 2); "
        "flag for review once a clinical collaborator joins.",
        "- **Age-anchor flags combine a life-stage keyword list (\"infant\", \"my "
        "toddler\", \"menopause\") with a numeric self-reported-age regex** "
        "(\"I'm 47\", \"17-year-old\", \"17 y/o\", \"29M\", \"22F\"). The numeric "
        "pattern was added after discovering that 56%+ of the 10,717-scenario "
        "pool already states an explicit age this way, and the keyword list "
        "alone caught under 4% of those -- an earlier version of this pool "
        "undercounted age-anchored scenarios substantially. Two follow-on gaps "
        "were also caught and fixed: a typographic apostrophe (\"I’m 16\", not "
        "\"I'm 16\") wasn't matched by the regex's literal `'`, and forum "
        "demographic shorthand (\"27M\", \"22F,\") wasn't covered by the \"N "
        "years old\" phrasings at all. Both are still first-pass heuristics, "
        "not a clinical judgment, and likely miss other phrasings (e.g. implied "
        "age from context like \"since I retired\" without the word "
        "\"retirement\"); spot-check before clinician review.",
        f"- Stratified sampling uses a fixed random seed ({RANDOM_SEED}) for "
        "reproducibility; per-category quotas are proportional to each "
        "category's share of the eligible pool, rounded up to at least 1 where "
        "the category is non-empty.",
    ]

    SELECTION_LOG_PATH.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pool-size", type=int, default=DEFAULT_POOL_SIZE)
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    args = parser.parse_args()

    curated_df = refine_scenario_pool(pool_size=args.pool_size, seed=args.seed)
    print(f"Wrote {CURATED_POOL_CSV_PATH} ({len(curated_df)} rows -- the curated pool)")
    print(f"Wrote {FULL_AUDIT_CSV_PATH} (full annotated pool, audit trail)")
    print(f"Wrote {SELECTION_LOG_PATH}")
