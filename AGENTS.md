# campania_transplant — agent instructions

Inherits global rules from `~/.codex/AGENTS.md` and `~/.cursor/rules/`. **Cursor mirror:** [`.cursor/rules/`](.cursor/rules/) — keep in sync with this file.

## Disk-efficient dependencies

- Use the repo-root `.venv` created by `uv venv --python 3.11 .venv`.
- Install with `uv pip install --python .\.venv\Scripts\python.exe --link-mode hardlink -r requirements.txt` so packages share physical data through the global `uv` cache.
- Keep the cache and repo on the same filesystem; avoid bare `pip`, copy mode, `--no-cache`, and routine `uv cache clean`.
## Purpose

Budget-impact model and interactive Streamlit dashboard for the Campania transplant / PIRP paper. Implements the equations from the source document (Appendix X and Table 17.1); users vary assumptions via sliders and pull dashboard numbers and figures into the manuscript.

Research / health-economics artifact only. Not clinical decision support.

## Stack

From [`requirements.txt`](requirements.txt):

- `streamlit>=1.28` — interactive dashboard.
- `matplotlib>=3.5` — charts and figure exports.
- `numpy>=1.20` — model numerics.
- `graphviz>=0.20` — schema diagrams (system `graphviz` listed in `packages.txt` for Streamlit Cloud).
- `python-docx>=0.8.11` — reads, diffs, and repairs the source paper DOCX.

Quick start:

```bash
uv venv --python 3.11 .venv
uv pip install --python .\.venv\Scripts\python.exe --link-mode hardlink -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the URL Streamlit prints (e.g. `http://localhost:8501`).

## Uses from global catalog

- **Office DOCX (preferred):** when **authoring or repairing** the source paper on Windows for review-grade output, **prefer Word COM**. Existing `scripts/repair_revised_docx.py` and similar may continue using `python-docx`, but new write paths should consider Word COM when the user is on Windows and quality matters.
- **Office DOCX (fallback):** `python-docx` is fine and currently used for diffing and extraction (`scripts/extract_docx.py`, `scripts/compare_docx_versions.py`, `scripts/map_docx_media.py`).
- **Streamlit + charts** stack from the global catalog.
- **Python numerics:** numpy / matplotlib already in use; add scipy or statsmodels only if a model change requires them.
- No PowerPoint, no `win32com` in this repo today.

## Layout

- [`app.py`](app.py) — Streamlit entrypoint; reads sliders, runs the engine, draws figures.
- `model/` — `params.py` (slider ranges and defaults), `engine.py` (budget-impact equations).
- `figures/` — `fig_costs.py`, `fig_savings.py`, `fig_model_schema.py` — matplotlib figure builders.
- `scripts/` — DOCX tooling:
  - [`extract_docx.py`](scripts/extract_docx.py) — pull text from the source paper.
  - [`compare_docx_versions.py`](scripts/compare_docx_versions.py) — version diff.
  - [`map_docx_media.py`](scripts/map_docx_media.py) — inventory embedded media.
  - [`repair_revised_docx.py`](scripts/repair_revised_docx.py) — fix structural issues in a revised DOCX.
  - `search_pdf_text.py` — text search across the supporting PDFs.
- `documents/` — source paper (`for troisi.docx`) and supporting material; treat as read-only inputs.

## Repo-specific rules

- The model equations are the source of truth in `model/engine.py`. When tuning numbers, keep code aligned with the paper (Appendix X / Table 17.1).
- Figures must regenerate cleanly from current slider state; never embed hand-tweaked figure files alongside the generators.
- Do not commit patient data, raw clinical exports, or unlicensed copies of third-party material.
- Streamlit Cloud deploys read `requirements.txt` and `packages.txt`; treat both as part of the lockstep.
- When DOCX writes degrade in `python-docx` (lost styling, broken track changes, malformed tables), refactor that script toward Word COM per the global preference.

## Verification (canonical checks for Verifier mode)

```powershell
uv pip install --python .\.venv\Scripts\python.exe --link-mode hardlink -r requirements.txt
.\.venv\Scripts\python.exe -m compileall model figures scripts app.py -q
```

**Manual / iterative UI:** exercising Streamlit sliders is inherently interactive—Planner should ask the user for a thumbs-up after dashboards change significantly.

### Known flaky

- **Graphviz** binary must exist locally for schema figures (see `requirements.txt` + `packages.txt` for hosting guidance).

## Repo skills catalog

Document iterative model + DOCX ingestion cycles in [`skills.md`](skills.md). **Cursor mirror:** also create `.cursor/skills/<name>/SKILL.md` when adding workflows.
## Stack propagation

When you introduce a new library, skill, or tool here, update `~/.codex/AGENTS.md` and propagate to other repos per global policy.

## Git

- Do not commit unless the user asks.
- Keep `documents/` and any locally cached PDFs / DOCX exports out of commits unless the user explicitly approves them.

<!-- BEGIN ORCHESTRATOR-MANAGED: knowledge-retrieval -->

## Orchestrator Knowledge (Optimized)
- Index-first: `C:\Users\ppyxe\Documents\GitHub\auto_learning_agent\knowledge\INDEX.md` then `C:\Users\ppyxe\Documents\GitHub\auto_learning_agent\knowledge\catalog.jsonl`.
- Repo-scoped retrieval: `C:\Users\ppyxe\Documents\GitHub\auto_learning_agent\scripts\retrieve_knowledge_for_repo.py --cwd C:\Users\ppyxe\Documents\GitHub\campania_transplant`.
- Open only shortlisted full records; repo `AGENTS.md` overrides catalog guidance.

<!-- END ORCHESTRATOR-MANAGED: knowledge-retrieval -->

<!-- BEGIN ORCHESTRATOR-MANAGED: graphify-policy -->

## Graphify architectural index

Use the governed federated Graphify graph first for repository orientation, architecture discovery, relationship tracing, symbol discovery, and locating likely implementation files. Query with `C:\Users\ppyxe\Documents\GitHub\auto_learning_agent\scripts\query_graph.py`; select `--repo <id>` for focused repository context.

Graphify is an index, not source of truth. Use actual source and `rg` for exact behavior, configuration, contracts, security-sensitive code, migrations, tests, assertions, error handling, and edits. Keep graphs local, respect `.graphifyignore`, and regenerate code-only graphs after material structural changes. Do not use remote, database, media, cloud, global-graph, or semantic-document features without repository-specific approval. Dirty graphs cannot justify knowledge promotion.

<!-- END ORCHESTRATOR-MANAGED: graphify-policy -->
