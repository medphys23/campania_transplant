# Campania Transplant Economic Model

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Budget impact](https://img.shields.io/badge/Budget%20impact-Health%20economics-2E7D32?style=flat-square)](https://www.ispor.org/)
[![Matplotlib](https://img.shields.io/badge/Charts-Matplotlib-11557c?style=flat-square&logo=matplotlib)](https://matplotlib.org/)

> Budget-impact model and interactive dashboard for the Campania transplant / PIRP paper. Implements the equations from the source document (Appendix X and Table 17.1). Vary assumptions via sliders and use the dashboard numbers and figures directly in your manuscript.

---

## Contents

- [Quick start](#quick-start)
- [What the app does](#what-the-app-does)
- [Model in depth](#model-in-depth)
- [Project structure](#project-structure)
- [Extracting the document](#extracting-the-document)
- [Requirements](#requirements)
- [Using the numbers in your paper](#using-the-numbers-in-your-paper)
- [Audit and checks](#audit-and-checks)

---

## 🚀 Quick start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the URL shown (e.g. `http://localhost:8501`). Change any slider—the dashboard and all figures update immediately (no Apply button).

**Deploy on Streamlit Community Cloud:** Connect your [GitHub repo](https://github.com/medphys23/campania_transplant) in [Streamlit Cloud](https://share.streamlit.io/). Use branch `main`, main file path `app.py`. The repo includes `requirements.txt` and `packages.txt` (for Graphviz).

---

## 📊 What the app does

| Feature | Description |
|--------|-------------|
| **Sidebar** | Sliders for all parameters (population, transplant rates, costs, PIRP reduction, pre-emptive share, discount rate, etc.) with wide min/max ranges for sensitivity. |
| **Key numbers** | Base values plus sensitivity ranges (dialysis ±€15k, tx year 1 ±€10k, tx year 2+ ±€2.5k)—e.g. *€25.5M* with *Range: €22.1M – €28.9M* underneath. |
| **Incident dialysis & PIRP impact** | New dialysis cases per year (200 pmp from document), cases avoided per year with PIRP, and € savings (avoided cases × dialysis cost). |
| **10-year savings by intervention** | Totals for PIRP, transplant expansion, pre-emptive, and combined (undiscounted for comparability). |
| **10-year dialysis cost projection** | BAU cost over 10 years, cost with PIRP only, cost with PIRP + transplant expansion, and total reduction vs BAU. |
| **Figures** | Tabs for Fig 12.1 (modality costs), 12.2 (model structure), 13.1 (cumulative cost per patient), 14.1 (ESKD distribution), 17.1–17.3 (savings by scenario). Each has a **Download PNG** button. |
| **3-year per-patient savings** | In an expander, with the same cost-sensitivity range. |

> **Note:** All series in Figure 17.3 use the same discounting so *Total* is always ≥ each component (PIRP only, transplant only).

---

## 📐 Model in depth

The economic model is a **deterministic cohort budget-impact model** from the perspective of the Campania regional healthcare payer. It estimates direct healthcare cost consequences of:

1. **Transplant expansion** — Scenario A and B targets (transplants per million population [pmp])
2. **PIRP** — Reducing incident ESKD via integrated CKD care
3. **Pre-emptive transplant** — Add-on savings

No health outcomes (QALYs, survival) are modelled—only costs and savings.

---

### Time horizon and discounting

- **Time horizon** *H*: default 10 years; configurable (e.g. 3–20) in the app.
- **Discount rate** *r*: when *r* > 0, future annual flows are discounted by 1/(1+*r*)^*t* in year *t*; cumulatives (`Cum_TOTAL_B`, `Cum_TX_B`, `Cum_PIRP`) are discounted. When *r* = 0, cumulatives are simple sums.
- The dashboard **10-year savings** and **10-year cost projection** use **undiscounted** totals for comparability; the main **10-yr cumulative (Scenario B)** in the key numbers uses the **discounted** series.

---

### Parameters (single source of truth: `model/params.py`)

| Symbol / key | Meaning | Base | Notes |
|--------------|--------|------|--------|
| `pop_m` | Campania population (millions) | 5.8 | AddTx and incident ESKD |
| `tx_pmp_baseline` | Current transplant rate (pmp) | 14.3 | Scenario B (35 pmp) ≈ 120 add’l tx/year |
| `tx_pmp_A` | Scenario A target (pmp) | 25 | Policy target |
| `tx_pmp_B` | Scenario B target (pmp) | 35 | Parity with Emilia-Romagna |
| `H` | Time horizon (years) | 10 | Budget impact window |
| `c_dial` | Annual dialysis cost (€/patient) | 50 000 | All-in maintenance dialysis |
| `c_tx1` | Transplant year 1 cost (€) | 60 000 | Index episode + follow-up |
| `c_txm` | Transplant year 2+ cost (€) | 12 000 | Immunosuppression + outpatient |
| `inc_pmp` | Incident ESKD (pmp/year) | 200 | Campania baseline (document) |
| `pirp_r` | PIRP incidence reduction (share) | 0.10 | e.g. 10% fewer new dialysis starts |
| `preempt_share` | Share of add’l transplants that are pre-emptive | 0.20 | Applied to AddTx |
| `preempt_delta` | Incremental saving per pre-emptive tx (€, one-time) | 20 000 | Add-on to transplant savings |
| `n_dial` | Prevalent dialysis population | 6 500 | Current burden, Fig 14.1 |
| `r_disc` | Annual discount rate | 0.03 | 0 = undiscounted |

Slider ranges in the app are wider than Table 17.1 (e.g. dialysis 30k–80k, tx Y1 40k–100k) for sensitivity exploration.

---

### Core equations (implemented in `model/engine.py`)

**Additional transplants per year (by scenario)**

$$\text{AddTx}_s = \max\left(0,\; (\text{TxTarget}_s - \text{TxBaseline}) \times \text{Pop}_M\right)$$

Population in millions; result in patients per year. Same formula for Scenario A and B with their respective targets.

**Per-patient cumulative costs (dialysis vs transplant)**

- Dialysis over *t* years: CumDial(*t*) = *t* × *c*_dial
- Transplant over *t* years: CumTx(*t*) = *c*_tx1 + (*t*−1) × *c*_txm
- Break-even year: *t*_be = ⌈(*c*_tx1 − *c*_txm) / (*c*_dial − *c*_txm)⌉ (calendar year, 1-based)

**Annual savings from transplant expansion (year *t*)**

$$S_{\text{TX}}(t) = \text{AddTx} \times \left[ (c_{\text{dial}} - c_{\text{tx1}}) + (t-1)(c_{\text{dial}} - c_{\text{txm}}) \right]$$

Year 1 can be negative (upfront cost); from year 2 onward *S*_TX(*t*) becomes positive and increasing.

**Incident dialysis and PIRP savings**

- New dialysis cases/year (baseline): **Incident** = Pop_M × inc_pmp (e.g. 5.8 × 200 = 1 160)
- Cases avoided/year with PIRP: **AvoidInc** = Pop_M × inc_pmp × *r*_PIRP
- Annual PIRP savings (€): **S_PIRP** = AvoidInc × *c*_dial

**Pre-emptive add-on**

$$S_{\text{PRE}} = \text{AddTx} \times \text{preempt\_share} \times \Delta_{\text{PRE}}$$

Constant each year (same AddTx every year).

**Total annual savings (Scenario B)**

$$S_{\text{TOTAL}}(t) = S_{\text{TX}}(t) + S_{\text{PIRP}} + S_{\text{PRE}}$$

*S*_PIRP and *S*_PRE do not depend on *t*; *S*_TX(*t*) does.

**Cumulative series (with optional discounting)**

- *r* = 0: cumulative = sum of annual flows from year 1 to *t*
- *r* > 0: each year’s flow × 1/(1+*r*)^*t*, then cumulated. Engine returns `Cum_TOTAL_A`, `Cum_TOTAL_B`, `Cum_BAU`, `Cum_TX_B`, `Cum_PIRP` (same discounting so Total ≥ each component in Fig 17.3)

**Current dialysis burden (annual)**

$$\text{Burden} = n_{\text{dial}} \times c_{\text{dial}}$$

Used for current burden and 10-year BAU projection (10 × Burden).

---

### Scenarios and BAU

| Term | Meaning |
|-----|--------|
| **Scenario A / B** | Same model, different transplant targets → different AddTx, *S*_TX, *S*_PRE, and totals |
| **BAU (in engine)** | Scenario B transplant flow but **no** PIRP (*S*_TX + *S*_PRE only). “Transplant + Pre-emptive (no PIRP)” in Fig 17.3 |
| **True BAU** | No interventions; AddTx = 0, PIRP = 0 → savings = 0 (flat line in Fig 17.3) |

---

### 10-year projections (dashboard)

| Metric | Formula |
|--------|--------|
| Total BAU dialysis cost (10 yr) | 10 × Burden |
| 10-yr savings PIRP | 10 × *S*_PIRP |
| 10-yr savings transplant expansion | Σ*t*=1..10 *S*_TX(*t*) (undiscounted) |
| 10-yr savings pre-emptive | 10 × *S*_PRE |
| 10-yr total savings (all) | Σ*t*=1..10 *S*_TOTAL(*t*) (undiscounted) |
| Projected cost with PIRP only | BAU total − 10×PIRP savings |
| Projected cost with PIRP + transplants | BAU total − total 10-yr savings |

---

### Engine output (`annual_and_cumulative`)

Returns a dict with:

- **Annual series** (length *H*): `S_TX_A`, `S_TX_B`, `S_PIRP`, `S_PRE_A`, `S_PRE_B`, `S_TOTAL_A`, `S_TOTAL_B`, `S_BAU`
- **Cumulative** (discounted if *r* > 0): `Cum_TOTAL_A`, `Cum_TOTAL_B`, `Cum_BAU`, `Cum_TX_B`, `Cum_PIRP`
- **Scalars**: `years`, `avg_annual_A`, `avg_annual_B`, `avg_s_tx_B`, `annual_s_pirp`, `annual_s_pre_B`

Figures and the dashboard read from this dict and the same parameter set so all displayed values are consistent.

---

## 📁 Project structure

| Path | Description |
|------|-------------|
| `app.py` | Streamlit app: sliders, dashboard (metrics + ranges + incident/PIRP + 10-yr projections), figure tabs, PNG download |
| `model/params.py` | Parameter definitions and min/max ranges (single source of truth) |
| `model/engine.py` | All formulas: AddTx, S_TX, S_PIRP, S_PRE, cumulative (optional discounting), break-even, burden, Cum_TX_B, Cum_PIRP |
| `figures/` | Matplotlib: `fig_costs.py` (12.1, 13.1, 14.1), `fig_model_schema.py` (12.2), `fig_savings.py` (17.1–17.3) |
| `scripts/extract_docx.py` | Extracts `documents/campania_transplant_final.docx` → `documents/campania_transplant_extracted.md` |
| `documents/` | Source docx, extracted markdown, and `AUDIT_REPORT.md` |

---

## 📄 Extracting the document

Regenerate the extracted text and tables from the Word document:

```bash
pip install -r requirements.txt
python scripts/extract_docx.py
```

**Output:** `documents/campania_transplant_extracted.md`  
**Input:** defaults to `documents/campania_transplant_final.docx`; you can pass paths as arguments.

---

## 📦 Requirements

- **Python** 3.8+
- **Packages:** see `requirements.txt` — `python-docx`, `graphviz`, `matplotlib`, `numpy`, `streamlit`

---

## 📝 Using the numbers in your paper

- Use the **Key numbers** section for main outputs (with ranges). Cite the sensitivity assumption (dialysis ±€15k, tx Y1 ±€10k, tx Y2+ ±€2.5k).
- **Incident dialysis & PIRP impact** and **10-year savings / projection** give the incident-case logic and BAU vs PIRP vs PIRP+transplants in one place.
- Export figures via **Download PNG** in the figure tabs and drop them into the manuscript.

---

## ✅ Audit and checks

**[documents/AUDIT_REPORT.md](documents/AUDIT_REPORT.md)** summarises calculation checks, graph suggestions, and extended insights from the audit of the original document. The model implements the document formulas; the audit notes where the text had inconsistencies (e.g. PIRP €6M vs formula €58M) so you can align the paper narrative.
