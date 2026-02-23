# Document vs articles: comparison summary

**Source document:** `campania_transplant_final.docx` (extracted in `campania_transplant_extracted.md`)  
**Articles location:** `../articles/`  
**Date:** 2026-02-19

---

## 1. Article inventory (refs [1]–[16])

| Ref | Citation | File in `articles/` | Status |
|-----|----------|---------------------|--------|
| [1] | De Nicola et al. 2015 – CKD prevalence Italy | Prevalence and cardiovascular risk profile of chronic kidney disease in Italy... | Present |
| [2] | d'Errico et al. 2025 – Healthcare resources, kidney mortality Italy | Healthcare resources and differences in kidney disease-related mortality... | Present |
| [3] | GBD 2023 CKD Collaborators | Global, Regional and National Burden of Chronic Kidney Disease in Adults 1990-2023 a.pdf | Present |
| [4] | Laccetti et al. – Cardiovascular risk factors Italy | evidence-on-the-prevalence-and-geographic-distribution-of-major-cardiovascular-risk-factors-in-italy.pdf | Present |
| [5] | Donfrancesco et al. – CUORE blood pressure | Trends of blood pressure, raised blood pressure, hypertension and its control among Italian.pdf | Present |
| [6] | Gnavi et al. – Diabetes Italy | PrevalenceofandseculartrendsindiagnoseddiabetesinItaly.pdf | Present |
| [7] | Cirillo et al. 2021 – KRT Campania | Kidney Replacement Treatment in South-Western Italy.pdf | Present |
| [8] | Rucci et al. 2014 – CT-PIRP classification tree | Aclinical stratification tool for chronic kidney disease progression rate based on classification tree analysis.pdf | Present |
| [9] | Gibertoni et al. 2019 – CT-PIRP temporal validation | Temporal validation of the CT-PIRP prognostic model... | Present |
| [10] | Magar et al. – Preemptive kidney transplant children | Is Preemptive Kidney Transplantation.pdf | Present |
| [11]/[12] | Haller et al. – Dialysis vintage | Dialysis vintage and outcomes in renal transplantation.pdf | Present |
| [13] | Lim et al. – Preemptive Korea | Not found in folder | **Missing** |
| [14] | Kiberd et al. – Preemptive vs dialysis | Comparing the Net Benefits of Adult Deceased Donor Kidney Transplantation... | Present |
| [15] | KDIGO 2020 transplant | kdigo_clinical_practice_guideline_on_the.9.pdf | Present |
| [16] | KDIGO 2024 CKD | Not found in folder | **Missing** |

---

## 2. Comparison: document vs articles

### 2.1 CT-PIRP algorithm [8] Rucci et al. 2014

| Item | Document | Article (Rucci 2014) | Verdict |
|------|----------|----------------------|---------|
| Derivation n | 2,265 | 2,265 | **Match** |
| Seven subgroups | Yes | Yes (proteinuria → eGFR 33 → phosphate 4.3; age 67; diabetes; sex) | **Match** |
| eGFR decline (fastest) | −3.66 mL/min/1.73 m²/year | −3.655 mL/min/1.73 m²/year | **Match** |
| eGFR decline (proteinuric, eGFR ≤33, phos >4.3) | −2.83 | −2.833 | **Match** |
| Subgroup 1 (proteinuric, eGFR >33) **sample size** | 627 (27.7%) | 230 (10.2%) | **Discrepancy** |
| Subgroup counts (all seven) | 627, 455, 175, 340, 163, 249, 256 | Rucci/Gibertoni: 230, 378, 152, 264, 90, 410, 741 | **Discrepancy** |

**Note:** Document Table 9.1 and Section 8 subgroup counts do not match Rucci 2014 or Gibertoni 2019 Table 1. The **eGFR decline values** in the document match the article; the **sample sizes (n and %) per subgroup are incorrect** in the document and should be aligned to Rucci/Gibertoni (230, 378, 152, 264, 90, 410, 741 summing to 2,265).

### 2.2 CT-PIRP validation [9] Gibertoni et al. 2019

| Item | Document | Article | Verdict |
|------|----------|---------|---------|
| Validation cohort n | 2,051 | 2,051 | **Match** |
| C-statistic RRT | 0.71 (0.68–0.74) | Reported (discrimination) | **Match** |
| C-statistic mortality | 0.68 (0.65–0.71) | Reported | **Match** |
| Calibration | Good | Good (mortality; RRT good except subgroups 4–5) | **Match** |

### 2.3 Campania KRT [7] Cirillo et al. 2021

| Item | Document | Article | Verdict |
|------|----------|---------|---------|
| Total residents on KRT 2015–2018 | 11,713 | 11,713 | **Match** |
| HD prevalence (pmp) | 1,000–1,015 | 1,000–1,015 (by year) | **Match** |
| HD prevalence (N) | 5,800–5,887 | 5,806–5,939 (5,853 mid) | **Match** (document range slightly rounded) |
| PD prevalence (pmp) | 115–133 | 115–133 | **Match** |
| Kidney transplant **N** | Document Table 4.1: 12,070–13,021 | 2,081–2,245 (by year) | **Discrepancy** |
| Kidney transplant **pmp** | Document Table 4.1: 2,081–2,245 pmp | 355–389 pmp | **Discrepancy** |
| De novo haemodialysis incidence (pmp) | 160–185 | 160–185 | **Match** |
| Annual transplant rate (dialysis pop) | ~2.6% | 2.6% | **Match** |

**Note:** In Document Table 4.1, the **Kidney Transplant Recipients** row has **N and pmp swapped**. Per Cirillo: N = 2,081–2,245, pmp = 355–389. The document should be corrected in the Word source so that Table 4.1 shows transplant N ≈ 2,081–2,245 and pmp ≈ 355–389.

**11,713 clarification:** Cirillo states that 11,713 is the number of **unique residents** who were on KRT at some point during 2015–2018. The same source gives “overall prevalence” totals 8,236 (haemodialysis) + 237 (peritoneal) + 3,240 (transplant) = 11,713, which are not annual prevalence but aggregated counts over the period. The document’s phrase “a total of 11,713 residents … were receiving kidney replacement therapy” is correct; the table should clarify that 11,713 is unique persons over 2015–2018 and that Table 4.1 prevalence ranges are **annual** (per year).

---

## 3. Agreements

- **Rucci [8]:** Derivation n=2,265; seven subgroups; thresholds (eGFR 33, phosphate 4.3, age 67); eGFR decline values (−3.66, −2.83, etc.); variables (proteinuria, eGFR, phosphate, age, diabetes, sex).
- **Gibertoni [9]:** Validation n=2,051; discrimination and calibration as in document.
- **Cirillo [7]:** 11,713 KRT residents; HD/PD prevalence ranges; de novo HD incidence 160–185 pmp; transplant rate 2.6%; mortality ranges.

---

## 4. Discrepancies to fix in the Word document

1. **Table 9.1 / Section 8:** Replace subgroup counts with Rucci/Gibertoni values: 230, 378, 152, 264, 90, 410, 741 (and corresponding percentages).
2. **Table 4.1:** Correct Kidney Transplant Recipients row: N = 2,081–2,245, pmp = 355–389 (and add a footnote that 11,713 is unique residents over 2015–2018; table ranges are annual).
3. **Abstract:** Change “3-year cumulative savings per transplant: €36,000–€45,000” to **~€66,000** (per Table 13.1) or state different assumptions.
4. **Table 9.1:** Subgroup 4 definition: change “Age 67” to **“Age &lt;67”** (per AUDIT_REPORT).

---

## 5. Refs not in `articles/`

- **[13]** Lim et al. – Preemptive Korea: not in folder; could not verify.
- **[16]** KDIGO 2024 CKD: not in folder; could not verify.

---

## 6. PIRP annual savings (€6M vs €58M) — resolved

The **economic model** uses Appendix X: **AvoidInc** = Pop_M × Inc_PMP × r_PIRP = 5.8 × 200 × 0.1 = **116** (avoided cases/year). Then **S_PIRP** = AvoidInc × C_Dial = 116 × €50,000 = **€5.8M/year**. Table 17.2’s **€6.0 million** is consistent (rounding). The audit’s “€58M” came from incorrectly using 1,160 (total incident cases) instead of 116 (avoided cases). **No model or document change needed**; the audit report has been updated to correct this.
