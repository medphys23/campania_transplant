"""
Fig 12.2: Economic model structure — three modules contributing to total savings.s
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import Dict


def fig_12_2(values: Dict, results: Dict) -> plt.Figure:
    """Schematic: Transplant expansion, PIRP, Pre-emptive → Total savings; annotate with € amounts."""
    avg_tx = results.get("avg_s_tx_B") or 0
    s_pirp = results.get("annual_s_pirp") or 0
    s_pre = results.get("annual_s_pre_B") or 0
    total = avg_tx + s_pirp + s_pre

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.set_aspect("equal")
    ax.axis("off")

    def box(ax, x, y, w, h, label, value_m):
        rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", facecolor="lightblue", edgecolor="navy")
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2 + 0.15, label, ha="center", va="center", fontsize=10)
        ax.text(x + w / 2, y + h / 2 - 0.15, f"€{value_m:.1f}M/yr", ha="center", va="center", fontsize=9)

    box(ax, 0.5, 1.5, 2.2, 1.0, "Transplant expansion", avg_tx / 1e6)
    box(ax, 3.8, 1.5, 2.2, 1.0, "PIRP incidence reduction", s_pirp / 1e6)
    box(ax, 7.1, 1.5, 2.2, 1.0, "Pre-emptive add-on", s_pre / 1e6)
    # Exact values below each box
    ax.text(1.6, 1.0, f"€{avg_tx:,.0f}", ha="center", fontsize=8)
    ax.text(4.9, 1.0, f"€{s_pirp:,.0f}", ha="center", fontsize=8)
    ax.text(8.2, 1.0, f"€{s_pre:,.0f}", ha="center", fontsize=8)

    ax.annotate("", xy=(5.0, 0.8), xytext=(5.0, 0.5), arrowprops=dict(arrowstyle="->", color="black"))
    ax.text(5.0, 0.35, f"Total ≈ €{total/1e6:.1f}M/year\n(€{total:,.0f})", ha="center", fontsize=10, fontweight="bold")

    ax.set_title("Economic model structure: three modules contribute to total savings")
    fig.tight_layout()
    return fig
