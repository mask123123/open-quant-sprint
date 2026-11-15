"""Square-root market impact as a per-row fee for run_backtest, by Yukun (Track 14).

The cost of trading Q notional is priced as one parent order worked over about an hour:

    impact = (2/3) * y * sigma_d * sqrt(Q / V_d),    Q = aum * turnover

with sigma_d the daily volatility and V_d the daily quote volume of the symbol. It goes into the
backtest without touching it:

    fee = 5.0 + np.nan_to_num(impact_bps(df, weights, aum))
    run_backtest(df, weights, fee_bps=fee)

Every value at row t uses only bars of the same symbol before t, since the trade charged on row t
is made at the close of bar t - 1. Like run_backtest, the functions expect df sorted by
(timestamp, symbol) with one row per symbol and hour, and return one value per row of df.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.backtest import coerce_weights


def turnover(df: pd.DataFrame, weights, lag_bars: int = 1) -> np.ndarray:
    """Turnover that run_backtest charges on each row; the lines are copied from run_backtest."""
    if lag_bars < 1:
        raise ValueError(f"lag_bars must be >= 1 to prevent same-bar execution leak, got {lag_bars}")

    work = df[["timestamp", "symbol"]].copy()
    work["w_raw"] = coerce_weights(df, weights).to_numpy(dtype=np.float64)

    gross = work["w_raw"].abs().groupby(work["timestamp"]).transform("sum")
    scale = np.where(gross > 1.0, 1.0 / gross, 1.0)
    work["w"] = work["w_raw"] * scale

    work["w_held"] = work.groupby("symbol")["w"].shift(lag_bars).fillna(0.0)
    work["w_prev_held"] = work.groupby("symbol")["w_held"].shift(1).fillna(0.0)
    return (work["w_held"] - work["w_prev_held"]).abs().to_numpy(dtype=np.float64)


def daily_sigma_volume(df: pd.DataFrame, days: int = 30) -> tuple[np.ndarray, np.ndarray]:
    """Daily volatility and daily quote volume per row, from the last 24 * days bars before it.

    sigma_d: sample std (ddof=1) of hourly log returns times sqrt(24); at row t with days=30, the
    720 returns between the closes of bars t - 721 and t - 1.
    V_d: mean quote_volume of bars t - 720 to t - 1, times 24.
    Both need at least 24 observations (min_periods=24), so sigma_d is NaN on the first 25 bars of
    a symbol and V_d on the first 24.
    """
    if days < 1 or int(days) != days:
        raise ValueError(f"days must be a positive integer, got {days}")
    window = 24 * int(days)
    symbol = df["symbol"]

    log_ret = np.log(df["close"]).groupby(symbol).diff()
    sigma = log_ret.groupby(symbol).transform(
        lambda x: x.rolling(window, min_periods=24).std(ddof=1).shift(1)
    ) * np.sqrt(24)
    volume = df["quote_volume"].groupby(symbol).transform(
        lambda x: x.rolling(window, min_periods=24).mean().shift(1)
    ) * 24
    return sigma.to_numpy(dtype=np.float64), volume.to_numpy(dtype=np.float64)


def impact_bps(
    df: pd.DataFrame,
    weights,
    aum: float,
    y: float = 1.0,
    days: int = 30,
    lag_bars: int = 1,
) -> np.ndarray:
    """Average square-root impact in bps of the notional traded on each row.

    0 where the turnover is 0. NaN where the turnover is positive but sigma_d or V_d is not
    available (the first 25 bars of a symbol) or V_d is 0. aum and quote_volume are in USDT.
    """
    if not aum > 0:
        raise ValueError(f"aum must be positive, got {aum}")
    if not y >= 0:
        raise ValueError(f"y must be non-negative, got {y}")

    to = turnover(df, weights, lag_bars)
    sigma, volume = daily_sigma_volume(df, days)
    volume = np.where(volume > 0, volume, np.nan)  # no traded volume, no estimate (not inf)

    cost = (2.0 / 3.0) * y * sigma * np.sqrt(aum * to / volume) * 1e4
    return np.where(to > 0, cost, 0.0)
