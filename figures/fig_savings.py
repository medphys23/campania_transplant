"""
Fig 17.1: Ten-year cumulative savings by transplant expansion scenario.s
Fig 17.2: Annual savings by intervention type (transplant, PIRP, pre-emptive).
Fig 17.3: Ten-year cumulative savings — PIRP vs BAU.
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict


def fig_17_1(values: Dict, results: Dict) -> plt.Figure:
    """Line plot: cumulative savings over 10 years for Scenario A and Scenario B."""
    years = results["years"]
    cum_A = results["Cum_TOTAL_A"]
    cum_B = results["Cum_TOTAL_B"]
    H = len(years)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(years, cum_A / 1e6, "o-", label=f"Scenario A: {int(values['tx_pmp_A'])} pmp", color="C0", linewidth=2, markersize=8)
    ax.plot(years, cum_B / 1e6, "s-", label=f"Scenario B: {int(values['tx_pmp_B'])} pmp", color="C1", linewidth=2, markersize=8)
    for i, (yA, yB) in enumerate(zip(cum_A / 1e6, cum_B / 1e6)):
        ax.annotate(f"€{yA:.1f}M", (years[i], yA), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=7)
        ax.annotate(f"€{yB:.1f}M", (years[i], yB), textcoords="offset points", xytext=(0, -10), ha="center", fontsize=7)
    ax.set_xlabel("Year")
    ax.set_ylabel("Cumulative savings (EUR millions)")
    ax.set_title("Ten-year cumulative savings by transplant expansion scenario")
    ax.set_ylim(0, None)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xticks(years.astype(int))
    fig.tight_layout()
    return fig


def fig_17_2(values: Dict, results: Dict) -> plt.Figure:
    """Stacked or grouped bar: average annual savings by component (transplant, PIRP, pre-emptive)."""
    avg_B = results["avg_annual_B"]
    s_pirp = results["annual_s_pirp"]
    s_pre = results["annual_s_pre_B"]
    s_tx_avg = results.get("avg_s_tx_B") or (avg_B - s_pirp - s_pre)

    fig, ax = plt.subplots(figsize=(6, 4))
    labels = ["Transplant expansion", "PIRP incidence reduction", "Pre-emptive add-on"]
    amounts = [s_tx_avg, s_pirp, s_pre]
    colors = ["C0", "C1", "C2"]
    x = np.arange(len(labels))
    bars = ax.bar(x, [a / 1e6 for a in amounts], color=colors, edgecolor="black", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15, ha="right")
    ax.set_ylabel("Average annual savings (EUR millions)")
    ax.set_title("Annual savings by intervention type (Scenario B, years 1–10)")
    ax.set_ylim(0, None)
    for b, a in zip(bars, amounts):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.2, f"€{a/1e6:.2f}M\n({a:,.0f})", ha="center", fontsize=8)
    fig.tight_layout()
    return fig


def fig_17_3(values: Dict, results: Dict) -> plt.Figure:
    """Line plot: True BAU, PIRP only, Transplant expansion only, Total (all). All use same discount."""
    years = results["years"]
    cum_true_bau = np.zeros_like(years)
    cum_pirp_only = results["Cum_PIRP"]         # Discounted cumulative PIRP only
    cum_tx_only = results["Cum_TX_B"]           # Discounted cumulative transplant expansion only
    cum_total = results["Cum_TOTAL_B"]          # Discounted total of all contributions

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, cum_true_bau / 1e6, "^-", label="True BAU (no interventions)", color="red", linewidth=2.5, markersize=8, linestyle="-")
    ax.plot(years, cum_pirp_only / 1e6, "v-", label="PIRP only (standalone)", color="C3", linewidth=2, markersize=7)
    ax.plot(years, cum_tx_only / 1e6, "s-", label="Transplant expansion only (core)", color="C1", linewidth=2, markersize=7)
    ax.plot(years, cum_total / 1e6, "o-", label="Total (all contributions)", color="C0", linewidth=2.5, markersize=8)
    for i in range(len(years)):
        ax.annotate(f"€{cum_total[i]/1e6:.1f}M", (years[i], cum_total[i] / 1e6), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=6, fontweight="bold")
        ax.annotate(f"€{cum_tx_only[i]/1e6:.1f}M", (years[i], cum_tx_only[i] / 1e6), textcoords="offset points", xytext=(0, -8), ha="center", fontsize=6)
        ax.annotate(f"€{cum_pirp_only[i]/1e6:.1f}M", (years[i], cum_pirp_only[i] / 1e6), textcoords="offset points", xytext=(0, -11), ha="center", fontsize=6)
    ax.set_xlabel("Year")
    ax.set_ylabel("Cumulative savings (EUR millions)")
    ax.set_title("Ten-year cumulative savings: True BAU → PIRP only → Transplant only → Total")
    ax.set_ylim(0, None)
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(years.astype(int))
    fig.tight_layout()
    return fig
