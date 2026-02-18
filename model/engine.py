"""
Economic model engine: all equations from Appendix X and document Sections 12–17.
Pure functions; no GUI or plotting.
"""
import numpy as np
from typing import Dict, Tuple


def add_tx(tx_pmp_target: float, tx_pmp_baseline: float, pop_m: float) -> float:
    """Additional transplants per year: (TxTarget - TxBaseline) * Pop_M (millions)."""
    return max(0.0, (tx_pmp_target - tx_pmp_baseline) * pop_m)


def cumulative_costs_patient(
    years: int, c_dial: float, c_tx1: float, c_txm: float
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per-patient cumulative dialysis, transplant, and difference (years 1..years)."""
    t = np.arange(1, years + 1, dtype=float)
    cum_dial = t * c_dial
    cum_tx = c_tx1 + (t - 1) * c_txm
    diff = cum_tx - cum_dial  # negative = savings
    return cum_dial, cum_tx, diff


def break_even_year(c_dial: float, c_tx1: float, c_txm: float) -> float:
    """Calendar year (1-based) after which transplant is cost-saving. (c_tx1 - c_dial) / (c_dial - c_txm)."""
    denom = c_dial - c_txm
    if denom <= 0:
        return 1.0
    t_be = (c_tx1 - c_dial) / denom
    # Break-even in cumulative sense: year where cum_tx < cum_dial
    # cum_dial(t) = t*c_dial, cum_tx(t) = c_tx1 + (t-1)*c_txm. Solve t*c_dial = c_tx1 + (t-1)*c_txm -> t = (c_tx1 - c_txm) / (c_dial - c_txm)
    t_cal = (c_tx1 - c_txm) / denom
    return max(1.0, np.ceil(t_cal))


def savings_tx(
    t: int, add_tx: float, c_dial: float, c_tx1: float, c_txm: float
) -> float:
    """S_TX(t) = AddTx * [(C_Dial - C_Tx1) + (t-1)*(C_Dial - C_TxMaint)]."""
    return add_tx * ((c_dial - c_tx1) + (t - 1) * (c_dial - c_txm))


def savings_pirp(pop_m: float, inc_pmp: float, pirp_r: float, c_dial: float) -> float:
    """AvoidInc = pop_m * inc_pmp * pirp_r; S_PIRP = AvoidInc * c_dial (annual)."""
    avoid_inc = pop_m * inc_pmp * pirp_r
    return avoid_inc * c_dial


def savings_pre(add_tx: float, preempt_share: float, preempt_delta: float) -> float:
    """S_PRE = AddTx * preempt_share * preempt_delta (constant each year in flow model)."""
    return add_tx * preempt_share * preempt_delta


def current_burden(n_dial: float, c_dial: float) -> float:
    """Annual dialysis expenditure (EUR)."""
    return n_dial * c_dial


def annual_and_cumulative(
    H: int,
    add_tx_a: float,
    add_tx_b: float,
    c_dial: float,
    c_tx1: float,
    c_txm: float,
    pop_m: float,
    inc_pmp: float,
    pirp_r: float,
    preempt_share: float,
    preempt_delta: float,
    r_disc: float = 0.0,
) -> Dict:
    """
    Time series for Scenario A, B, and BAU.
    Returns dict with arrays: years, S_TX_A, S_TX_B, S_PIRP, S_PRE_A, S_PRE_B,
    S_TOTAL_A, S_TOTAL_B, Cum_TOTAL_A, Cum_TOTAL_B, Cum_BAU (no PIRP, Scenario B flow).
    """
    years_arr = np.arange(1, H + 1, dtype=float)
    n = len(years_arr)

    S_TX_A = np.array([savings_tx(int(t), add_tx_a, c_dial, c_tx1, c_txm) for t in years_arr])
    S_TX_B = np.array([savings_tx(int(t), add_tx_b, c_dial, c_tx1, c_txm) for t in years_arr])
    s_pirp = savings_pirp(pop_m, inc_pmp, pirp_r, c_dial)
    S_PIRP = np.full(n, s_pirp)
    S_PRE_A = np.full(n, savings_pre(add_tx_a, preempt_share, preempt_delta))
    S_PRE_B = np.full(n, savings_pre(add_tx_b, preempt_share, preempt_delta))

    S_TOTAL_A = S_TX_A + S_PIRP + S_PRE_A
    S_TOTAL_B = S_TX_B + S_PIRP + S_PRE_B
    S_BAU = S_TX_B + S_PRE_B  # no PIRP

    def cumdisc(arr: np.ndarray) -> np.ndarray:
        if r_disc <= 0:
            return np.cumsum(arr)
        disc = np.array([1.0 / ((1.0 + r_disc) ** t) for t in years_arr])
        return np.cumsum(arr * disc)

    Cum_TOTAL_A = cumdisc(S_TOTAL_A)
    Cum_TOTAL_B = cumdisc(S_TOTAL_B)
    Cum_BAU = cumdisc(S_BAU)
    Cum_TX_B = cumdisc(S_TX_B)
    Cum_PIRP = cumdisc(S_PIRP)

    avg_annual_A = np.sum(S_TOTAL_A) / H
    avg_annual_B = np.sum(S_TOTAL_B) / H
    avg_s_tx_B = np.mean(S_TX_B)

    return {
        "years": years_arr,
        "S_TX_A": S_TX_A,
        "S_TX_B": S_TX_B,
        "S_PIRP": S_PIRP,
        "S_PRE_A": S_PRE_A,
        "S_PRE_B": S_PRE_B,
        "S_TOTAL_A": S_TOTAL_A,
        "S_TOTAL_B": S_TOTAL_B,
        "S_BAU": S_BAU,
        "Cum_TOTAL_A": Cum_TOTAL_A,
        "Cum_TOTAL_B": Cum_TOTAL_B,
        "Cum_BAU": Cum_BAU,
        "Cum_TX_B": Cum_TX_B,
        "Cum_PIRP": Cum_PIRP,
        "avg_annual_A": avg_annual_A,
        "avg_annual_B": avg_annual_B,
        "avg_s_tx_B": avg_s_tx_B,
        "annual_s_pirp": s_pirp,
        "annual_s_pre_B": float(S_PRE_B[0]),
    }
