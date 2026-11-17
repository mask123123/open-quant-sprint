"""Track 14 Part 2 (#21): square-root impact against the flat and tiered fees.

Implements the choices preregistered in the draft PR (valiyevoktay-cmd/open-quant-sprint#42):
y = 1, days = 30, lag_bars = 1, aum in {1e5, ..., 1e8}, NaN impact set to 0, a trade is a row with
|weight_change| > 1e-12, merged runs with gap 0 (step 3) and gap 3 (step 4).

    python -m research.yukun.part2 --data data/train_1h.parquet --out research/yukun/results_train.md
    python -m research.yukun.part2 --synthetic --out <file>      # dry run on generated data
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from src.backtest import run_backtest, tiered_fee_bps
from src.contrib.yukun import daily_sigma_volume, impact_bps, run_impact_cost, turnover, weight_change
from src.sandbox import load_module_fn

AUMS = [1e5, 3e5, 1e6, 3e6, 1e7, 3e7, 1e8]
STRATEGIES = ["template", "baseline_flow", "angelo_closeloc"]
FLAT_BPS = 5.0
TOL = 1e-12
GAPS = {"hourly": None, "merged (gap 0)": 0, "merged (gap 3)": 3}


def md(t: pd.DataFrame) -> str:
    """Markdown table without the tabulate dependency."""
    cells = [[str(t.index.name or "")] + [str(c) for c in t.columns]]
    for idx, row in zip(t.index, t.to_numpy()):  # a few dozen rows of results, not the panel
        cells.append([f"{idx:.4g}" if isinstance(idx, float) else str(idx)] + [f"{v:.4g}" for v in row])
    lines = ["| " + " | ".join(r) + " |" for r in cells]
    return "\n".join([lines[0], "|" + "---|" * len(cells[0])] + lines[1:])


def per_symbol_table(df: pd.DataFrame, sigma: np.ndarray, volume: np.ndarray, tier: np.ndarray) -> pd.DataFrame:
    ok = np.isfinite(sigma) & np.isfinite(volume)
    t = pd.DataFrame({"symbol": df["symbol"].to_numpy(), "sigma_d": sigma, "V_d": volume, "tier_bps": tier})[ok]
    out = t.groupby("symbol").median()
    out["Q*"] = out["V_d"] * (1.5 * FLAT_BPS * 1e-4 / out["sigma_d"]) ** 2
    out["cost_index"] = out["sigma_d"] / np.sqrt(out["V_d"])  # cost of a fixed trade is proportional
    return out.sort_values("cost_index", ascending=False)


def follow_shares(df: pd.DataFrame, change: np.ndarray, to: np.ndarray) -> tuple[float, float]:
    """Shares of traded notional where the same symbol traded in the bar before, same / opposite way."""
    sign = pd.Series(np.where(np.abs(change) > TOL, np.sign(change), 0.0), index=df.index)
    prev = sign.groupby(df["symbol"]).shift(1).fillna(0.0).to_numpy()
    sign = sign.to_numpy()
    traded = to[sign != 0].sum()
    return to[(sign != 0) & (prev == sign)].sum() / traded, to[(sign != 0) & (prev == -sign)].sum() / traded


def strategy_tables(df: pd.DataFrame, w: np.ndarray, volume: np.ndarray, tier: np.ndarray) -> dict:
    change = weight_change(df, w)
    to = turnover(df, w)
    trade = np.abs(change) > TOL
    c5 = float((to * FLAT_BPS * 1e-4).sum())
    c_tier = float((to * tier * 1e-4).sum())
    same, opposite = follow_shares(df, change, to)

    flat = run_backtest(df, w, fee_bps=FLAT_BPS)
    tiered = run_backtest(df, w, fee_bps=tier)
    rows = []
    for aum in AUMS:
        imp = np.nan_to_num(impact_bps(df, w, aum))
        m = run_backtest(df, w, fee_bps=FLAT_BPS + imp)
        part = aum * to / volume
        known = trade & np.isfinite(part)
        rows.append(
            {
                "aum": aum,
                "sharpe_flat": flat.sharpe,
                "sharpe_tiered": tiered.sharpe,
                "sharpe_impact": m.sharpe,
                "avg_impact_bps": float((to * imp).sum() / to.sum()),
                "impact_cost": float((to * imp * 1e-4).sum()),
                "share_below_1e-4": float(to[known & (part < 1e-4)].sum() / to[known].sum()),
                "share_above_1pct": float(to[known & (part > 1e-2)].sum() / to[known].sum()),
            }
        )
    table = pd.DataFrame(rows).set_index("aum")

    breakeven = {}
    for label, gap in GAPS.items():
        if gap is None:
            i_1m = float(table.loc[1e6, "impact_cost"])
        else:
            i_1m = float(np.nansum(run_impact_cost(df, w, 1e6, gap=gap)))
        breakeven[label] = {
            "impact_cost_1M": i_1m,
            "aum_impact_eq_flat": 1e6 / (i_1m / c5) ** 2,
            "aum_flat_plus_impact_eq_tiered": 1e6 * ((c_tier - c5) / i_1m) ** 2,
        }

    return {
        "table": table,
        "breakeven": pd.DataFrame(breakeven).T,
        "c5": c5,
        "c_tier": c_tier,
        "c5_backtest": flat.fee_cost_cum,
        "c_tier_backtest": tiered.fee_cost_cum,
        "same": same,
        "opposite": opposite,
        "mean_turnover": float(to.sum() / df["timestamp"].nunique()),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path)
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    if args.synthetic:
        from data.build_dataset import generate_calibrated_panel

        df = generate_calibrated_panel(n_hours=3000, seed=7)
        label = "synthetic panel (generate_calibrated_panel, 3000 h, seed 7)"
    else:
        df = pd.read_parquet(args.data)
        label = str(args.data)
    df = df.sort_values(["timestamp", "symbol"]).reset_index(drop=True)

    sigma, volume = daily_sigma_volume(df)
    tier = tiered_fee_bps(df)
    sym = per_symbol_table(df, sigma, volume, tier)
    ratio = sym["cost_index"].iloc[0] / sym["cost_index"].iloc[-1]

    out = [f"# Track 14 Part 2 results: {label}", "", f"{df['symbol'].nunique()} symbols, {df['timestamp'].nunique()} hours, y = 1", ""]
    out += ["## Step 1: per symbol (medians)", "", md(sym), ""]
    out += [f"Cost of a fixed trade, most / least expensive symbol (sigma_d / sqrt(V_d)): {ratio:.2f}x; tiered fee ratio 10/5 = 2x", ""]

    for name in STRATEGIES:
        w = load_module_fn(Path("strategies") / f"{name}.py")(df.copy())
        w = np.asarray(pd.Series(w).reindex(df.index) if isinstance(w, pd.Series) else w, dtype=np.float64)
        r = strategy_tables(df, w, volume, tier)
        out += [f"## {name}", ""]
        out += [
            f"mean turnover per hour {r['mean_turnover']:.4g}; total fee cost (fraction of capital) at 5 bps "
            f"{r['c5']:.4g} (backtest {r['c5_backtest']}), tiered {r['c_tier']:.4g} (backtest {r['c_tier_backtest']})",
            f"shares of traded notional following a trade in the bar before: same direction {r['same']:.3f}, "
            f"opposite {r['opposite']:.3f}",
            "",
            md(r["table"]),
            "",
            md(r["breakeven"]),
            "",
        ]

    text = "\n".join(out)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
