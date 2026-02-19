"""
Parameter definitions with Low/Base/High ranges for GUI sliders.
Single source of truth for the economic model (Appendix X + Table 17.1).s
"""
from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class ParamRange:
    """Min, max, and current value for one parameter."""
    min_val: float
    max_val: float
    value: float

    def clamp(self) -> float:
        return max(self.min_val, min(self.max_val, self.value))


# Wider ranges for sliders (extended beyond Table 17.1 for sensitivity exploration)
def default_ranges() -> dict:
    return {
        "pop_m": ParamRange(2.0, 12.0, 5.8),
        "tx_pmp_baseline": ParamRange(5.0, 30.0, 14.3),
        "tx_pmp_A": ParamRange(15.0, 50.0, 25.0),
        "tx_pmp_B": ParamRange(20.0, 60.0, 35.0),
        "H": ParamRange(3.0, 20.0, 10.0),
        "c_dial": ParamRange(30_000.0, 80_000.0, 50_000.0),
        "c_tx1": ParamRange(40_000.0, 100_000.0, 60_000.0),
        "c_txm": ParamRange(5_000.0, 25_000.0, 12_000.0),
        "inc_pmp": ParamRange(80.0, 350.0, 200.0),
        "pirp_r": ParamRange(0.0, 0.30, 0.10),
        "preempt_share": ParamRange(0.0, 0.50, 0.20),
        "preempt_delta": ParamRange(5_000.0, 50_000.0, 20_000.0),
        "n_dial": ParamRange(2_000.0, 15_000.0, 6_500.0),
        "r_disc": ParamRange(0.0, 0.10, 0.03),
    }


def get_values(ranges: dict) -> dict:
    """Extract current (clamped) values for engine/figures."""
    return {k: r.value for k, r in ranges.items()}


# Modality costs for Fig 12.1 (Table 12.1) — midpoints of document ranges
MODALITY_LABELS = [
    "In-centre haemodialysis",
    "Home haemodialysis",
    "Peritoneal dialysis",
    "Kidney transplant (Year 1)",
    "Kidney transplant (Year 2+)",
]


def modality_costs_from_params(values: dict) -> list:
    """Annual cost per modality; last two from c_tx1, c_txm; first from c_dial."""
    return [
        values["c_dial"],
        (35_000 + 45_000) / 2,  # Home HD range
        (30_000 + 40_000) / 2,  # PD range
        values["c_tx1"],
        values["c_txm"],
    ]
