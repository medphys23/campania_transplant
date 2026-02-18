"""
Campania transplant economic model — Streamlit GUI.
Sliders for all parameters (min/max from plan); figures update on every change (fluid).
"""
import io
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from model.params import default_ranges, get_values
from model import engine
from figures import fig_costs, fig_model_schema, fig_savings

# Cost sensitivity deltas for dashboard ranges (reporting)
DELTA_C_DIAL = 15_000
DELTA_C_TX1 = 10_000
DELTA_C_TXM = 2_500

st.set_page_config(page_title="Campania transplant model", layout="wide")

# Initialize or restore ranges in session state
if "ranges" not in st.session_state:
    st.session_state.ranges = default_ranges()

ranges = st.session_state.ranges

# ----- Sidebar: sliders -----
st.sidebar.title("Model parameters")
st.sidebar.caption("Change any slider; figures and summary update immediately.")

with st.sidebar.expander("Demography", expanded=True):
    ranges["pop_m"].value = st.slider(
        "Population (millions)",
        min_value=float(ranges["pop_m"].min_val),
        max_value=float(ranges["pop_m"].max_val),
        value=float(ranges["pop_m"].value),
        step=0.1,
        key="pop_m",
    )
    ranges["tx_pmp_baseline"].value = st.slider(
        "Baseline transplant rate (pmp)",
        min_value=float(ranges["tx_pmp_baseline"].min_val),
        max_value=float(ranges["tx_pmp_baseline"].max_val),
        value=float(ranges["tx_pmp_baseline"].value),
        step=0.5,
        key="tx_pmp_baseline",
    )
    ranges["n_dial"].value = st.slider(
        "Prevalent dialysis N",
        min_value=float(ranges["n_dial"].min_val),
        max_value=float(ranges["n_dial"].max_val),
        value=float(ranges["n_dial"].value),
        step=100.0,
        key="n_dial",
    )

with st.sidebar.expander("Scenarios", expanded=True):
    ranges["tx_pmp_A"].value = st.slider(
        "Scenario A target (pmp)",
        min_value=float(ranges["tx_pmp_A"].min_val),
        max_value=float(ranges["tx_pmp_A"].max_val),
        value=float(ranges["tx_pmp_A"].value),
        step=1.0,
        key="tx_pmp_A",
    )
    ranges["tx_pmp_B"].value = st.slider(
        "Scenario B target (pmp)",
        min_value=float(ranges["tx_pmp_B"].min_val),
        max_value=float(ranges["tx_pmp_B"].max_val),
        value=float(ranges["tx_pmp_B"].value),
        step=1.0,
        key="tx_pmp_B",
    )
    ranges["H"].value = st.slider(
        "Time horizon (years)",
        min_value=int(ranges["H"].min_val),
        max_value=int(ranges["H"].max_val),
        value=int(ranges["H"].value),
        step=1,
        key="H",
    )

with st.sidebar.expander("Costs (EUR)", expanded=True):
    ranges["c_dial"].value = st.slider(
        "Annual dialysis cost",
        min_value=int(ranges["c_dial"].min_val),
        max_value=int(ranges["c_dial"].max_val),
        value=int(ranges["c_dial"].value),
        step=1000,
        key="c_dial",
    )
    ranges["c_tx1"].value = st.slider(
        "Transplant year 1 cost",
        min_value=int(ranges["c_tx1"].min_val),
        max_value=int(ranges["c_tx1"].max_val),
        value=int(ranges["c_tx1"].value),
        step=1000,
        key="c_tx1",
    )
    ranges["c_txm"].value = st.slider(
        "Transplant year 2+ cost",
        min_value=int(ranges["c_txm"].min_val),
        max_value=int(ranges["c_txm"].max_val),
        value=int(ranges["c_txm"].value),
        step=500,
        key="c_txm",
    )

with st.sidebar.expander("PIRP & incidence", expanded=True):
    ranges["inc_pmp"].value = st.slider(
        "Incident ESKD (pmp/year)",
        min_value=float(ranges["inc_pmp"].min_val),
        max_value=float(ranges["inc_pmp"].max_val),
        value=float(ranges["inc_pmp"].value),
        step=10.0,
        key="inc_pmp",
    )
    ranges["pirp_r"].value = st.slider(
        "PIRP incidence reduction (share)",
        min_value=float(ranges["pirp_r"].min_val),
        max_value=float(ranges["pirp_r"].max_val),
        value=float(ranges["pirp_r"].value),
        step=0.01,
        format="%.2f",
        key="pirp_r",
    )

with st.sidebar.expander("Pre-emptive", expanded=True):
    ranges["preempt_share"].value = st.slider(
        "Pre-emptive share (of add'l transplants)",
        min_value=float(ranges["preempt_share"].min_val),
        max_value=float(ranges["preempt_share"].max_val),
        value=float(ranges["preempt_share"].value),
        step=0.05,
        format="%.2f",
        key="preempt_share",
    )
    ranges["preempt_delta"].value = st.slider(
        "Incremental saving per pre-emptive tx (EUR)",
        min_value=int(ranges["preempt_delta"].min_val),
        max_value=int(ranges["preempt_delta"].max_val),
        value=int(ranges["preempt_delta"].value),
        step=1000,
        key="preempt_delta",
    )

with st.sidebar.expander("Discount rate", expanded=False):
    ranges["r_disc"].value = st.slider(
        "Discount rate",
        min_value=float(ranges["r_disc"].min_val),
        max_value=float(ranges["r_disc"].max_val),
        value=float(ranges["r_disc"].value),
        step=0.01,
        format="%.2f",
        key="r_disc",
    )

# ----- Current values for engine -----
values = get_values(ranges)
H = int(values["H"])
pop_m = values["pop_m"]
c_dial = values["c_dial"]
c_tx1 = values["c_tx1"]
c_txm = values["c_txm"]
inc_pmp = values["inc_pmp"]
pirp_r = values["pirp_r"]
preempt_share = values["preempt_share"]
preempt_delta = values["preempt_delta"]
r_disc = values["r_disc"]

add_tx_a = engine.add_tx(values["tx_pmp_A"], values["tx_pmp_baseline"], pop_m)
add_tx_b = engine.add_tx(values["tx_pmp_B"], values["tx_pmp_baseline"], pop_m)
t_be = engine.break_even_year(c_dial, c_tx1, c_txm)
burden = engine.current_burden(values["n_dial"], c_dial)

results = engine.annual_and_cumulative(
    H, add_tx_a, add_tx_b, c_dial, c_tx1, c_txm,
    pop_m, inc_pmp, pirp_r, preempt_share, preempt_delta, r_disc,
)

# Low/high cost scenarios (clamped to slider bounds) for sensitivity ranges
c_dial_low = max(float(ranges["c_dial"].min_val), c_dial - DELTA_C_DIAL)
c_dial_high = min(float(ranges["c_dial"].max_val), c_dial + DELTA_C_DIAL)
c_tx1_low = max(float(ranges["c_tx1"].min_val), c_tx1 - DELTA_C_TX1)
c_tx1_high = min(float(ranges["c_tx1"].max_val), c_tx1 + DELTA_C_TX1)
c_txm_low = max(float(ranges["c_txm"].min_val), c_txm - DELTA_C_TXM)
c_txm_high = min(float(ranges["c_txm"].max_val), c_txm + DELTA_C_TXM)

results_low = engine.annual_and_cumulative(
    H, add_tx_a, add_tx_b, c_dial_low, c_tx1_low, c_txm_low,
    pop_m, inc_pmp, pirp_r, preempt_share, preempt_delta, r_disc,
)
results_high = engine.annual_and_cumulative(
    H, add_tx_a, add_tx_b, c_dial_high, c_tx1_high, c_txm_high,
    pop_m, inc_pmp, pirp_r, preempt_share, preempt_delta, r_disc,
)
t_be_low = engine.break_even_year(c_dial_low, c_tx1_low, c_txm_low)
t_be_high = engine.break_even_year(c_dial_high, c_tx1_high, c_txm_high)
burden_low = engine.current_burden(values["n_dial"], c_dial_low)
burden_high = engine.current_burden(values["n_dial"], c_dial_high)

def _range_str(base, low, high, decimals=1, prefix="", suffix=""):
    lo, hi = min(base, low, high), max(base, low, high)
    return f"{prefix}{lo:.{decimals}f}{suffix} – {prefix}{hi:.{decimals}f}{suffix}"

# Incident dialysis (from document: inc_pmp = 200 pmp, baseline = pop_m × inc_pmp)
incident_eskd_per_year = int(round(pop_m * inc_pmp))
avoided_with_pirp_per_year = int(round(pop_m * inc_pmp * pirp_r))
# PIRP actual savings = avoided cases × cost per dialysis (used in model)
annual_pirp_savings = results["annual_s_pirp"]

# 10-year totals: BAU cost and savings by source (undiscounted for projection)
burden_10yr_bau = 10 * burden
pirp_reduction_10yr = 10 * annual_pirp_savings
savings_10yr_tx = float(np.sum(results["S_TX_B"]))
savings_10yr_pre = 10 * results["annual_s_pre_B"]
savings_10yr_total = float(np.sum(results["S_TOTAL_B"]))
burden_10yr_with_pirp = burden_10yr_bau - pirp_reduction_10yr
burden_10yr_with_all = burden_10yr_bau - savings_10yr_total

# ----- Main: summary table -----
st.title("Campania transplant economic model")
st.caption("Key numbers (use these in your paper). Ranges: dialysis ±€15k, tx Y1 ±€10k, tx Y2+ ±€2.5k.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Add'l transplants (Scenario A)", f"{add_tx_a:.0f}/year")
    st.metric("Add'l transplants (Scenario B)", f"{add_tx_b:.0f}/year")
with col2:
    st.metric("Break-even year", f"{t_be:.1f}")
    st.caption(f"Range: {_range_str(t_be, t_be_low, t_be_high, decimals=1)}")
    st.metric("Current dialysis burden", f"€{burden/1e6:.0f}M/year")
    st.caption(f"Range: €{min(burden, burden_low, burden_high)/1e6:.0f} – €{max(burden, burden_low, burden_high)/1e6:.0f}M/year")
with col3:
    avg_b = results["avg_annual_B"] / 1e6
    avg_b_lo = results_low["avg_annual_B"] / 1e6
    avg_b_hi = results_high["avg_annual_B"] / 1e6
    st.metric("Avg annual savings (Scenario B)", f"€{avg_b:.2f}M")
    st.caption(f"Range: {_range_str(avg_b, avg_b_lo, avg_b_hi, prefix='€', suffix='M')}")
    cum_b = results["Cum_TOTAL_B"][-1] / 1e6
    cum_b_lo = results_low["Cum_TOTAL_B"][-1] / 1e6
    cum_b_hi = results_high["Cum_TOTAL_B"][-1] / 1e6
    st.metric("10-yr cumulative (Scenario B)", f"€{cum_b:.0f}M")
    st.caption(f"Range: {_range_str(cum_b, cum_b_lo, cum_b_hi, decimals=0, prefix='€', suffix='M')}")
with col4:
    pirp_b = results["annual_s_pirp"] / 1e6
    pirp_lo = results_low["annual_s_pirp"] / 1e6
    pirp_hi = results_high["annual_s_pirp"] / 1e6
    st.metric("PIRP annual (formula)", f"€{pirp_b:.1f}M")
    st.caption(f"Range: {_range_str(pirp_b, pirp_lo, pirp_hi, prefix='€', suffix='M')}")
    st.metric("Pre-emptive annual", f"€{results['annual_s_pre_B']/1e6:.2f}M")

# Incident dialysis & PIRP impact (from document: 200 pmp, PIRP reduces incident ESKD)
st.subheader("Incident dialysis & PIRP impact")
inc1, inc2, inc3 = st.columns(3)
with inc1:
    st.metric("New dialysis cases per year (baseline)", f"{incident_eskd_per_year:,}", help="From document: pop × 200 pmp (Campania baseline)")
with inc2:
    st.metric("Cases avoided per year with PIRP", f"{avoided_with_pirp_per_year:,}", help=f"PIRP incidence reduction r = {pirp_r*100:.0f}%")
with inc3:
    pct = (pirp_r * 100) if incident_eskd_per_year else 0
    st.metric("PIRP reduces new dialysis need by", f"{pct:.0f}% of baseline", help="Share of incident cases avoided with integrated CKD care")
st.caption("Actual PIRP savings in the model = avoided cases × dialysis cost per patient (€/year); this drives the PIRP annual € figure above.")

# 10-year savings by intervention (PIRP and expanded transplants)
st.subheader("10-year savings by intervention")
sav1, sav2, sav3, sav4 = st.columns(4)
with sav1:
    st.metric("10-yr savings: PIRP", f"€{pirp_reduction_10yr/1e6:.0f}M", help="10 × annual PIRP savings (fewer new dialysis starts)")
with sav2:
    st.metric("10-yr savings: Transplant expansion", f"€{savings_10yr_tx/1e6:.0f}M", help="Sum of annual savings from Scenario B transplant expansion")
with sav3:
    st.metric("10-yr savings: Pre-emptive", f"€{savings_10yr_pre/1e6:.0f}M", help="10 × annual pre-emptive add-on savings")
with sav4:
    st.metric("10-yr total savings (all)", f"€{savings_10yr_total/1e6:.0f}M", help="PIRP + transplant expansion + pre-emptive (undiscounted)")

# 10-year dialysis cost projection: BAU total and with interventions
st.subheader("10-year dialysis cost projection")
proj1, proj2, proj3, proj4 = st.columns(4)
with proj1:
    st.metric("Total BAU dialysis cost (10 yr)", f"€{burden_10yr_bau/1e6:.0f}M", help="10 × current annual dialysis burden (prevalent patients)")
with proj2:
    st.metric("With PIRP only (10 yr cost)", f"€{burden_10yr_with_pirp/1e6:.0f}M", help="BAU minus PIRP savings")
with proj3:
    st.metric("With PIRP + transplants (10 yr cost)", f"€{burden_10yr_with_all/1e6:.0f}M", help="BAU minus total savings (PIRP + transplant + pre-emptive)")
with proj4:
    st.metric("Total reduction vs BAU (10 yr)", f"€{savings_10yr_total/1e6:.0f}M", help="Combined savings from all interventions")

with st.expander("3-year per-patient savings (dialysis vs transplant)"):
    _, cum_d3, cum_t3 = engine.cumulative_costs_patient(3, c_dial, c_tx1, c_txm)
    sav3 = (cum_d3[-1] - cum_t3[-1]) / 1000
    sav3_low = (3 * c_dial_low - (c_tx1_low + 2 * c_txm_low)) / 1000
    sav3_hi = (3 * c_dial_high - (c_tx1_high + 2 * c_txm_high)) / 1000
    st.caption(_range_str(sav3, sav3_low, sav3_hi, decimals=0, prefix="€", suffix="k") + " (base and sensitivity range)")

# ----- Figures in tabs -----
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Fig 12.1 Modality costs",
    "Fig 12.2 Model structure",
    "Fig 13.1 Cumulative cost",
    "Fig 14.1 ESKD distribution",
    "Fig 17.1 Cumulative savings",
    "Fig 17.2 Annual by type",
    "Fig 17.3 PIRP vs BAU",
])

with tab1:
    fig = fig_costs.fig_12_1(values)
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    st.download_button("Download PNG", buf.getvalue(), "fig_12_1.png", "image/png")
    plt.close(fig)

with tab2:
    fig = fig_model_schema.fig_12_2(values, results)
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    st.download_button("Download PNG", buf.getvalue(), "fig_12_2.png", "image/png")
    plt.close(fig)

with tab3:
    fig = fig_costs.fig_13_1(values)
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    st.download_button("Download PNG", buf.getvalue(), "fig_13_1.png", "image/png")
    plt.close(fig)

with tab4:
    fig = fig_costs.fig_14_1(values)
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    st.download_button("Download PNG", buf.getvalue(), "fig_14_1.png", "image/png")
    plt.close(fig)

with tab5:
    fig = fig_savings.fig_17_1(values, results)
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    st.download_button("Download PNG", buf.getvalue(), "fig_17_1.png", "image/png")
    plt.close(fig)

with tab6:
    fig = fig_savings.fig_17_2(values, results)
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    st.download_button("Download PNG", buf.getvalue(), "fig_17_2.png", "image/png")
    plt.close(fig)

with tab7:
    fig = fig_savings.fig_17_3(values, results)
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    st.download_button("Download PNG", buf.getvalue(), "fig_17_3.png", "image/png")
    plt.close(fig)
