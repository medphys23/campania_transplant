"""
Fig 12.1: Annual per-patient cost by modality.
Fig 13.1: 10-year cumulative cost trajectories (dialysis vs transplant per patient).
Fig 14.1: Current annual ESKD cost distribution.
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List

from model.params import MODALITY_LABELS, modality_costs_from_params
from model import engine


def fig_12_1(values: Dict) -> plt.Figure:
    """Bar chart: annual per-patient cost by RRT modality (EUR)."""
    costs = modality_costs_from_params(values)
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(MODALITY_LABELS))
    bars = ax.bar(x, [c / 1000 for c in costs], color="steelblue", edgecolor="navy", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(MODALITY_LABELS, rotation=25, ha="right")
    ax.set_ylabel("Annual cost (EUR thousands)")
    ax.set_title("Annual per-patient costs by RRT modality (European data)")
    ax.set_ylim(0, None)
    ax.yaxis.grid(True, alpha=0.3)
    for b, c in zip(bars, costs):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.5, f"€{c/1000:.0f}k\n({c:,.0f})", ha="center", fontsize=8)
    fig.tight_layout()
    return fig


def fig_13_1(values: Dict) -> plt.Figure:
    """Line plot: 10-year cumulative dialysis vs transplant per patient; break-even."""
    H = int(values["H"])
    c_dial, c_tx1, c_txm = values["c_dial"], values["c_tx1"], values["c_txm"]
    cum_dial, cum_tx, diff = engine.cumulative_costs_patient(H, c_dial, c_tx1, c_txm)
    t_be = engine.break_even_year(c_dial, c_tx1, c_txm)

    fig, ax = plt.subplots(figsize=(8, 5))
    years = np.arange(1, H + 1)
    ax.plot(years, cum_dial / 1000, "o-", label="Dialysis", color="C0", linewidth=2, markersize=8)
    ax.plot(years, cum_tx / 1000, "s-", label="Transplant", color="C1", linewidth=2, markersize=8)
    for i, (yd, yt) in enumerate(zip(cum_dial / 1000, cum_tx / 1000)):
        ax.annotate(f"€{yd:.0f}k", (years[i], yd), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=7)
        ax.annotate(f"€{yt:.0f}k", (years[i], yt), textcoords="offset points", xytext=(0, -10), ha="center", fontsize=7)
    if 1 <= t_be <= H:
        ax.axvline(x=t_be, color="gray", linestyle="--", alpha=0.8, label=f"Break-even (year {int(t_be)})")
    ax.set_xlabel("Year")
    ax.set_ylabel("Cumulative cost (EUR thousands)")
    ax.set_title("10-year cumulative cost per patient: dialysis vs kidney transplantation")
    y_max = max(cum_dial.max(), cum_tx.max()) / 1000
    ax.set_ylim(0, y_max * 1.15)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xticks(years)
    fig.tight_layout()
    return fig


def fig_14_1(values: Dict) -> plt.Figure:
    """Current annual ESKD cost distribution (dialysis-dominated)."""
    n_dial = values["n_dial"]
    c_dial = values["c_dial"]
    total = engine.current_burden(n_dial, c_dial)
    labels = [f"Dialysis\n(n ≈ {int(n_dial):,})"]
    sizes = [total]
    colors = ["steelblue"]
    # Optional: add a small slice for "other" if desired; here just dialysis
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.pie(sizes, labels=labels, autopct=lambda p: f"€{total/1e6:.1f}M\n({total:,.0f})", colors=colors, startangle=90)
    ax.set_title(f"Current annual ESKD cost (Campania)\nTotal ≈ €{total/1e6:.0f} million (n_dial = {int(n_dial):,})")
    fig.tight_layout()
    return fig
