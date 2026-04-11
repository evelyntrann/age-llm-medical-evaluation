# Quantifying Age Bias in LLM-Generated Health Advice: Model Comparison and Safety Analysis

Codebase for studying how large language models answer health questions when prompts include age-related framing. The workflow builds an age-conditioned audit dataset, collects model responses (OpenAI batch API and local Llama), scores outputs with MedGemma, analyzes hidden-state embeddings, and computes bias and readability metrics.

Audit data also available on HuggingFace: [GPT Audited](https://huggingface.co/datasets/rileyhitthefan/healthqa_gpt_response_audit) and [Llama Audited](https://huggingface.co/datasets/rileyhitthefan/healthqa_llama_response_audit)

## Project overview and objectives

- **Goal:** Measure and compare **informational safety** and **age-related differential treatment** when models answer the same underlying health questions with different age cues (teen, young adult, middle-aged, senior) versus a neutral baseline.
- **Models:** OpenAI chat completions via **Batch API** (e.g. `gpt-5-mini` in the scripts) and **Llama 3.2 1B Instruct** via Hugging Face `transformers` on GPU.
- **Audit judge:** **MedGemma** (`google/medgemma-4b-it`) assigns discrete **safety** (1–5) and **severity** labels to free-text answers.
- **Analysis:** Custom metrics include **Age Differential Safety Bias (ADSB)** and **Safety Risk Score (SRS)** (`metrics/SafetyMetricsCalculator.py`), and **Tone Differential Index (TDI)** and related plots use `metrics/TDICalculator.py` (spaCy + readability features).

## Methodology / approach

1. **Prompt generation (`notebooks/01_prompt_generation.ipynb`):** Load base questions from HuggingFace (also exists in `data\base_prompts.csv`), use a local LLM pipeline to inject age framing, and export structured prompts to `data/gen_prompts.csv`.
2. **GPT responses (`notebooks/02_gpt_batch_inference.ipynb`):** Build a JSONL batch from `rileyhitthefan/age-based-health-qa`, submit OpenAI Batch jobs, parse results, and write `data/responses/response_gpt.csv` (and intermediate batch artifacts under `data/batch/` and `data/responses/`).
3. **Llama responses (`notebooks/03_llama_inference.ipynb`):** Run batched generation with Llama 3.2 1B Instruct on the same Hugging Face dataset; write `data/responses/response_llama.csv` (and extend as needed for full CSV exports).
4. **MedGemma audit (`notebooks/04_medgemma_safety_audit.ipynb`):** Load paired GPT/Llama response tables, run MedGemma to fill `safety_score_medgemma` and `severity_score_medgemma`, and save `data/responses/response_gpt_audit.csv` and `data/responses/response_llama_audit.csv`.
5. **Embeddings (`notebooks/05_embeddings_analysis.ipynb`):** Load audit prompts from `data/audit/`, compute layer-wise hidden states with Llama 3.2 1B, merge with MedGemma scores, and write tables and figures under `results/interpretation/` (and align with prior CSV exports in `results/embedding_analysis/` when present).
6. **Metrics (`notebooks/06_metrics_analysis.ipynb`):** Load audited responses, compute ADSB/SRS/TDI, and save plots and CSVs under `results/metrics/`.

## Repository layout

| Path | Role |
|------|------|
| `notebooks/` | Numbered notebooks `01_`–`06_` in pipeline order |
| `data/audit/` | Stacked audit prompts (e.g. `audit_gpt_1-53k.csv`) |
| `data/responses/` | Model outputs and MedGemma-scored audits |
| `data/batch/` | OpenAI batch input JSONL (created when you run step 2) |
| `results/interpretation/` | Embedding analysis exports (CSVs, parquet, figures) from notebook 05 |
| `results/embedding_analysis/` | Committed example tables from embedding runs |
| `results/metrics/` | Plots and TDI CSVs from notebook 06 |
| `metrics/` | Python modules `SafetyMetricsCalculator.py`, `TDICalculator.py` |
| `documents/` | Thesis and presentation materials (not required to run code) |

## Setup instructions and dependencies

### Environment

- **Python:** 3.11+.
- **Hardware:** NVIDIA GPU with sufficient VRAM for Llama 3.2 1B and MedGemma 4B; embedding notebook benefits from GPU memory for larger batch sizes.

### Install

```text
cd path/to/honors
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

### Credentials and access

- **Hugging Face:** Accept the license for `meta-llama/Llama-3.2-1B-Instruct` and `google/medgemma-4b-it`, then authenticate (`huggingface-cli login` or `HF_TOKEN` in the environment). Notebooks use `huggingface_hub.login()`; do **not** commit tokens to the repo.
- **OpenAI:** Set `OPENAI_API_KEY` (notebook 02 also shows loading from a `.env` file—point `load_dotenv` at your project or user `.env` as you prefer).

### Working directory

Run Jupyter with the **repository root** as the server root, or open notebooks from `notebooks/`; paths are written so that `../data/...` and `../results/...` resolve from inside `notebooks/`.

## Step-by-step: run the code

1. **Generate prompts:** Run `notebooks/01_prompt_generation.ipynb` end-to-end. Output: `data/gen_prompts.csv`.
2. **GPT batch:** Run `notebooks/02_gpt_batch_inference.ipynb`. Requires OpenAI API access and billing; batch jobs can take hours. Outputs land in `data/batch/` and `data/responses/`.
3. **Llama responses:** Run `notebooks/03_llama_inference.ipynb` on a CUDA machine with HF login. Adjust batch ranges to match your experiment size.
4. **MedGemma scoring:** Run `notebooks/04_medgemma_safety_audit.ipynb` after `response_gpt_1200.csv` / `response_llama_1200.csv` exist under `data/responses/`. Produces `response_*_audit_1200.csv` with safety and severity columns.
5. **Embeddings:** Run `notebooks/05_embeddings_analysis.ipynb` using `data/audit/audit_gpt_1-53k.csv` (or the audit file your study uses). Expect long GPU runs for full prompt sets; reduce `batch_size` or rows in development.
6. **Aggregate metrics:** Run `notebooks/06_metrics_analysis.ipynb`. The first cell adds the repo root to `sys.path` so `from metrics....` imports work from `notebooks/`.

## Summary of results and expected outputs (reproduction)

Use these checks to confirm each stage completed successfully.

| Stage | What to look for |
|--------|-------------------|
| **01** | `data/gen_prompts.csv` with age_group and prompt columns. |
| **02** | `data/batch/gpt_batch_1.jsonl`; after batch completion, parsed JSONL/TXT under `data/responses/` and `data/responses/response_gpt_1200.csv`. |
| **03** | `data/responses/test_4_2000.txt` (or your chosen export) with paired questions and answers. |
| **04** | `data/responses/response_gpt_audit_1200.csv` and `response_llama_audit_1200.csv` including `safety_score_medgemma` and `severity_score_medgemma`. |
| **05** | `results/interpretation/embeddings/prompt_embeddings_lastlayer.csv`, `results/interpretation/tables/*.csv`, and optional `figures/*.jpg` under `results/interpretation/`. |
| **06** | Console summaries for **ADSB** (per age group) and **SRS**; example statistics from a completed run showed negative mean ADSB on the order of **-0.14 to -0.17** across groups (see notebook output), with **unsafe_rate** near **0.6–0.8%** at threshold 3; **TDI** CSVs and plots under `results/metrics/`. |

---

If you previously had a Hugging Face token embedded in a notebook, revoke it in your [Hugging Face token settings](https://huggingface.co/settings/tokens) and use environment-based login going forward.
