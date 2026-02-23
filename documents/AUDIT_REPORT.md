# Audit Report: campania_transplant_final.docx

**Source:** Extracted content in `campania_transplant_extracted.md`  
**Scope:** Calculations, graphs, and extended insights.

---

## 1. Calculation checks

| Location | Statement / Numbers | Check | Verdict |
|----------|----------------------|--------|---------|
| Abstract | Annual dialysis €49,000–€89,000; post-transplant year 2+ €15,000–€30,000 | Table 12.1: in-centre HD €45k–€55k; transplant year 2+ €10k–€15k | **Minor:** Abstract uses wider ranges; table values are tighter and should be the reference. |
| Abstract | 3-year cumulative savings per transplant: €36,000–€45,000 | Table 13.1: Year 3 difference = €150,000 − €84,000 = **€66,000** per patient | **Needs correction:** Stated 3-year savings are too low; with document’s base-case costs, 3-year savings are ~€66,000. Clarify or correct abstract. |
| Section 2.2 | CKD prevalence 7.05%; G1–G2 4.16%, G3–G5 2.89%; “59% early-stage” | 4.16 + 2.89 = 7.05; 4.16/7.05 ≈ 59% | **OK** |
| Section 7.2 / Table 9.1 | Derivation cohort n = 2,265; subgroup counts and % | 627+455+175+340+163+249+256 = 2,265; each % matches n/2265 | **OK** |
| Section 4.2 / Table 4.1 | “11,713 residents receiving KRT”; table HD+PD+Tx ranges | Table ranges (e.g. 5887+771+13021) sum to ~19,679, not 11,713 | **Needs clarification:** Define whether 11,713 is dialysis-only or total KRT; clarify if table counts are additive or from different years/definitions. |
| Table 13.1 | Cumulative costs year 1–10 (dialysis vs transplant) | Year 2: 60+12=72; Year 3: 60+24=84; Year 10: 60+9×12=168; differences match | **OK** |
| Section 13.1 | Break-even “approximately 1–2 years” | With C_Dial=50k, C_Tx1=60k, C_TxM=12k, break-even in year 2 | **OK** |
| Section 14.1 | Annual dialysis expenditure €325 million | 6,500 × €50,000 = €325,000,000 | **OK** |
| Section 14.2 / Table 17.2 | Scenario B: 120 add’l transplants; €19.32M “annual savings” | 10-year cumulative / 10 ≈ €19.32M; AddTx = (35−14.3)×5.8 ≈ 120 | **OK** (interpret as average annual over 10 years). |
| Section 15.2 | PIRP: Avoided incident ESKD; “Annual Avoided Dialysis Cost” | AvoidInc = 5.8×200×0.1 = **116** (not 1,160); 116×€50,000 = **€5.8M/year**. Table 17.2 €6.0M is correct. | **OK** (audit’s earlier €58M was a miscalculation; see [DOCUMENT_VS_ARTICLES.md](DOCUMENT_VS_ARTICLES.md)). |
| Table 17.2 | Total €25.8M = 19.32 + 0.48 + 6.0 | Arithmetic correct given table values | **OK** (but total is conditional on PIRP figure above). |
| Section 16.1–16.2 | Diabetes 30% of 6,500 = 1,950; €97.5M. Hypertension 25% = 1,625; €81.25M | 1950×50k = 97.5M; 1625×50k = 81.25M | **OK** |
| Pre-emptive (Table 17.2) | €0.48 million | 120 × 0.2 × €20,000 = €0.48M | **OK** |
| Table 9.1 | Subgroup 4 definition | Cell says “Age 67” | **Minor:** Should read "Age &lt;67" for consistency with Section 8.5. |

**Summary:** One abstract correction (3-year savings), one clarification (KRT 11,713 vs table totals), and two minor fixes (abstract ranges; Table 9.1 “Age 67” → “Age &lt;67”). PIRP €6M is correct per formula (AvoidInc = 116); see [DOCUMENT_VS_ARTICLES.md](DOCUMENT_VS_ARTICLES.md).

---

## 2. Graph review

Figures are referenced by caption/title in the extracted text; chart data is not extractable from the .docx, so comments are based on stated purpose and best practice.

| Figure | Purpose (from document) | Assessment | Suggestions |
|--------|--------------------------|------------|-------------|
| **Figure 8.1** | CT-PIRP classification tree (seven risk subgroups) | Decision trees are appropriate. Structure matches Section 8 and Table 9.1. | Add n and % at each terminal node (e.g. “Subgroup 1, n=627, 27.7%”). Use one colour per risk tier (e.g. red/orange/yellow/green) for quick reading. Ensure root and splits are labelled with variable and threshold (e.g. “Proteinuria?”, “eGFR &gt;33?”). |
| **Figure 12.1** | Annual per-patient costs by RRT modality (European data) | Bar chart is appropriate for modality comparison. | Include sample size or source (e.g. “n studies” or “Campania/Italian tariffs”). Add 95% CIs or range bars if from multiple sources. Align order with Table 12.1 (HD, home HD, PD, Tx year 1, Tx year 2+). |
| **Figure 12.2** | Economic model structure (three modules → total savings) | Schematic is appropriate for model transparency. | Label the three modules explicitly (“Transplant expansion”, “PIRP incidence reduction”, “Pre-emptive add-on”). Add base-case annual amounts (e.g. €19.3M, €6M, €0.48M) on each branch so the total €25.8M is traceable. |
| **Figure 13.1** | 10-year cumulative cost trajectories (dialysis vs transplant per patient) | Line chart is appropriate for cumulative costs over time. | Start y-axis at 0; avoid truncation. Add a clear break-even marker (e.g. vertical line or annotation at year 2). Include a short caption note: “Base case: C_dial=€50k, C_tx1=€60k, C_txm=€12k.” |
| **Figure 14.1** | Current annual ESKD cost distribution in Campania | Distribution (e.g. by modality or category) is appropriate. | Define “current” (e.g. 2018 or 2020). If breakdown is by modality, include dialysis vs transplant and optionally “other”. Add total (e.g. “Total ≈ €325M”) and n (e.g. “N_dial ≈ 6,500”). |
| **Figure 17.1** | Ten-year cumulative savings by transplant expansion scenario | Cumulative savings over 10 years by scenario. | Label scenarios (e.g. “Scenario A: 25 pmp”, “Scenario B: 35 pmp”). Start y-axis at 0. Add legend and, if space, key parameter (e.g. AddTx per year). |
| **Figure 17.2** | Annual savings by intervention type (transplant, PIRP, pre-emptive) | Stacked or grouped bars by year and type. | Ensure three components are visually distinct and match Table 17.2 (transplant ~€19.3M, PIRP €6M, pre-emptive €0.48M once PIRP/transplant figures are reconciled). Add “Average annual (years 1–10)” if that is what is plotted. |
| **Figure 17.3** | Ten-year cumulative savings: PIRP incidence reduction vs BAU | Comparison of cumulative savings with vs without PIRP. | Label “PIRP (r=10%)” and “BAU”. Use same cost assumptions as in text. After reconciling PIRP (€6M vs €58M), ensure curve magnitudes match the chosen assumption. |

**Cross-cutting:** For all cost figures, state currency (EUR), discount rate if applied, and whether values are undiscounted or discounted. Adding “n” or “source” in captions improves reproducibility.

---

## 3. Extended insights

Concrete, document-specific suggestions that would add value without changing the main narrative:

1. **Subgroup-level cost and transplant impact**  
   The seven CT-PIRP subgroups have very different RRT risks and mortality. A **summary table or small dashboard** could show, per subgroup: (a) share of Campania CKD population (if estimable), (b) expected proportion progressing to RRT in 5 years, (c) suggested prioritization for transplant referral (e.g. Subgroups 2 and 3). This would link the clinical algorithm directly to resource use and transplant targeting.

2. **Sensitivity of total savings to PIRP magnitude**  
   The current sensitivity table (Table 17.1) varies PIRP incidence reduction (5%, 10%, 15%). Once the PIRP annual savings are reconciled (€6M vs €58M), add a **one-way sensitivity on the PIRP savings figure** (e.g. low/base/high) and show the effect on total annual savings (e.g. tornado or bar). This would make the impact of PIRP assumptions explicit and policy-relevant.

3. **Time trend and equity in one view**  
   The document cites gender and geographic disparities (e.g. HR for transplant access, suburban vs urban). A **single figure** could combine: (a) trend in dialysis incidence or transplant rate in Campania over 2015–2018 (or latest), and (b) a simple equity metric (e.g. transplant rate or referral rate by gender and/or area). This would support the “healthcare resources and disparities” narrative and baseline for evaluating the proposed intervention.

4. **Flow diagram from CKD to RRT**  
   A **CONSORT-style or pathway diagram** would clarify: (a) CKD population (e.g. Stage 3–5), (b) proportion entering PIRP-like care vs usual care, (c) incident dialysis and incident transplant, (d) pre-emptive vs non–pre-emptive transplant. Numbers could be approximate (e.g. from Section 4 and 14). This would make the “incident flow” model and the place of pre-emptive transplantation easier to follow for policymakers.

5. **One-page “key numbers” summary**  
   The document is long and dense. A **single summary table or infographic** with 8–12 headline numbers (e.g. ESKD incidence 200 pmp, N_dial ~6,500, current transplant rate, target 35 pmp, total potential savings €25.8M/year, break-even ~year 2, PIRP r=10%, pre-emptive share 20%) would help readers quickly grasp the main epidemiological and economic messages. It could sit after the Abstract or in the Conclusions.

---

## 4. Deliverables summary

| Deliverable | Location |
|-------------|----------|
| Extracted text and tables | [documents/campania_transplant_extracted.md](campania_transplant_extracted.md) |
| Extraction script | [scripts/extract_docx.py](../scripts/extract_docx.py) |
| This audit (calculations, graphs, insights) | This file |

4. **Document vs articles:** See [DOCUMENT_VS_ARTICLES.md](DOCUMENT_VS_ARTICLES.md) for comparison to source articles (Rucci, Gibertoni, Cirillo, etc.) and discrepancies to fix in the Word document (Table 9.1 subgroup n; Table 4.1 transplant N/pmp; abstract 3-year savings).
