# Track 14 Part 2 results: data/train_1h.parquet

20 symbols, 14871 hours, y = 1

## Step 1: per symbol (medians)

| symbol | sigma_d | V_d | tier_bps | Q* | cost_index |
|---|---|---|---|---|---|
| INJUSDT | 0.05324 | 6.545e+07 | 10 | 1.299e+04 | 6.581e-06 |
| OPUSDT | 0.04959 | 7.177e+07 | 10 | 1.641e+04 | 5.854e-06 |
| ATOMUSDT | 0.03725 | 4.235e+07 | 10 | 1.716e+04 | 5.725e-06 |
| ARBUSDT | 0.04938 | 7.897e+07 | 10 | 1.822e+04 | 5.556e-06 |
| APTUSDT | 0.04578 | 7.88e+07 | 10 | 2.114e+04 | 5.158e-06 |
| UNIUSDT | 0.05003 | 1.227e+08 | 7 | 2.757e+04 | 4.517e-06 |
| NEARUSDT | 0.04801 | 1.347e+08 | 7 | 3.289e+04 | 4.136e-06 |
| AAVEUSDT | 0.04684 | 1.642e+08 | 7 | 4.21e+04 | 3.655e-06 |
| DOTUSDT | 0.04156 | 1.3e+08 | 7 | 4.234e+04 | 3.645e-06 |
| AVAXUSDT | 0.04181 | 2.513e+08 | 7 | 8.087e+04 | 2.637e-06 |
| LINKUSDT | 0.04081 | 2.657e+08 | 7 | 8.974e+04 | 2.504e-06 |
| LTCUSDT | 0.03511 | 2.007e+08 | 7 | 9.162e+04 | 2.478e-06 |
| ADAUSDT | 0.04331 | 3.53e+08 | 7 | 1.058e+05 | 2.306e-06 |
| SUIUSDT | 0.04693 | 5.913e+08 | 7 | 1.51e+05 | 1.93e-06 |
| DOGEUSDT | 0.04197 | 9.525e+08 | 7 | 3.042e+05 | 1.36e-06 |
| BNBUSDT | 0.02317 | 4.861e+08 | 7 | 5.092e+05 | 1.051e-06 |
| XRPUSDT | 0.03539 | 1.468e+09 | 7 | 6.595e+05 | 9.235e-07 |
| SOLUSDT | 0.03782 | 3.218e+09 | 7 | 1.266e+06 | 6.667e-07 |
| ETHUSDT | 0.0344 | 1.129e+10 | 5 | 5.365e+06 | 3.238e-07 |
| BTCUSDT | 0.02144 | 1.51e+10 | 5 | 1.848e+07 | 1.745e-07 |

Cost of a fixed trade, most / least expensive symbol (sigma_d / sqrt(V_d)): 37.72x; tiered fee ratio 10/5 = 2x

## template

mean turnover per hour 0.07408; total fee cost (fraction of capital) at 5 bps 0.5508 (backtest 0.5508), tiered 0.8475 (backtest 0.8475)
shares of traded notional following a trade in the bar before: same direction 0.353, opposite 0.219

| aum | sharpe_flat | sharpe_tiered | sharpe_impact | avg_impact_bps | impact_cost | share_below_1e-4 | share_above_1pct |
|---|---|---|---|---|---|---|---|
| 1e+05 | -0.542 | -1.441 | -0.844 | 0.9045 | 0.09964 | 0.9808 | 0 |
| 3e+05 | -0.542 | -1.441 | -1.065 | 1.567 | 0.1726 | 0.8688 | 0 |
| 1e+06 | -0.542 | -1.441 | -1.497 | 2.86 | 0.3151 | 0.5703 | 0 |
| 3e+06 | -0.542 | -1.441 | -2.195 | 4.954 | 0.5457 | 0.3493 | 0 |
| 1e+07 | -0.542 | -1.441 | -3.558 | 9.045 | 0.9964 | 0.2094 | 0.01915 |
| 3e+07 | -0.542 | -1.441 | -5.763 | 15.67 | 1.726 | 0.1284 | 0.1312 |
| 1e+08 | -0.542 | -1.441 | -10.06 | 28.6 | 3.151 | 0.03456 | 0.4297 |

|  | impact_cost_1M | aum_impact_eq_flat | aum_flat_plus_impact_eq_tiered |
|---|---|---|---|
| hourly | 0.3151 | 3.056e+06 | 8.867e+05 |
| merged (gap 0) | 0.4118 | 1.789e+06 | 5.191e+05 |
| merged (gap 3) | 0.5693 | 9.361e+05 | 2.716e+05 |

## baseline_flow

mean turnover per hour 0.05219; total fee cost (fraction of capital) at 5 bps 0.388 (backtest 0.388), tiered 0.5944 (backtest 0.5944)
shares of traded notional following a trade in the bar before: same direction 0.347, opposite 0.247

| aum | sharpe_flat | sharpe_tiered | sharpe_impact | avg_impact_bps | impact_cost | share_below_1e-4 | share_above_1pct |
|---|---|---|---|---|---|---|---|
| 1e+05 | -1.534 | -2.288 | -1.749 | 0.7588 | 0.05889 | 0.991 | 0 |
| 3e+05 | -1.534 | -2.288 | -1.907 | 1.314 | 0.102 | 0.909 | 0 |
| 1e+06 | -1.534 | -2.288 | -2.214 | 2.4 | 0.1862 | 0.6454 | 0 |
| 3e+06 | -1.534 | -2.288 | -2.712 | 4.156 | 0.3226 | 0.3942 | 0 |
| 1e+07 | -1.534 | -2.288 | -3.684 | 7.588 | 0.5889 | 0.2421 | 0.009031 |
| 3e+07 | -1.534 | -2.288 | -5.255 | 13.14 | 1.02 | 0.1606 | 0.09104 |
| 1e+08 | -1.534 | -2.288 | -8.318 | 24 | 1.862 | 0.06748 | 0.3546 |

|  | impact_cost_1M | aum_impact_eq_flat | aum_flat_plus_impact_eq_tiered |
|---|---|---|---|
| hourly | 0.1862 | 4.341e+06 | 1.227e+06 |
| merged (gap 0) | 0.23 | 2.847e+06 | 8.048e+05 |
| merged (gap 3) | 0.3099 | 1.568e+06 | 4.432e+05 |

## angelo_closeloc

mean turnover per hour 0.7232; total fee cost (fraction of capital) at 5 bps 5.378 (backtest 5.3777), tiered 8.413 (backtest 8.4125)
shares of traded notional following a trade in the bar before: same direction 0.383, opposite 0.552

| aum | sharpe_flat | sharpe_tiered | sharpe_impact | avg_impact_bps | impact_cost | share_below_1e-4 | share_above_1pct |
|---|---|---|---|---|---|---|---|
| 1e+05 | -17.51 | -28.15 | -24.77 | 1.931 | 2.076 | 0.7976 | 0 |
| 3e+05 | -17.51 | -28.15 | -30.01 | 3.344 | 3.596 | 0.535 | 0 |
| 1e+06 | -17.51 | -28.15 | -40.03 | 6.105 | 6.566 | 0.2849 | 0.002678 |
| 3e+06 | -17.51 | -28.15 | -55.43 | 10.57 | 11.37 | 0.1625 | 0.04089 |
| 1e+07 | -17.51 | -28.15 | -81.67 | 19.31 | 20.76 | 0.09228 | 0.2024 |
| 3e+07 | -17.51 | -28.15 | -112.4 | 33.44 | 35.96 | 0.03645 | 0.465 |
| 1e+08 | -17.51 | -28.15 | -142.6 | 61.05 | 65.66 | 0.002102 | 0.7151 |

|  | impact_cost_1M | aum_impact_eq_flat | aum_flat_plus_impact_eq_tiered |
|---|---|---|---|
| hourly | 6.566 | 6.708e+05 | 2.136e+05 |
| merged (gap 0) | 8.266 | 4.232e+05 | 1.348e+05 |
| merged (gap 3) | 8.432 | 4.068e+05 | 1.295e+05 |
